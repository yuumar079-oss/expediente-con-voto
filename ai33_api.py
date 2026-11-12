"""AI33 v3: tareas persistentes; nunca reenvía automáticamente un POST ambiguo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = 'https://api.ai33.pro'
SKILL = Path(__file__).resolve().parent


def clave():
    value = os.environ.get('AI33_API_KEY', '').strip()
    if not value:
        path = SKILL / '.env'
        if path.exists():
            for line in path.read_text(encoding='utf-8-sig').splitlines():
                if line.strip().startswith('AI33_API_KEY='):
                    value = line.split('=', 1)[1].strip().strip('\"\'')
    if not value:
        raise SystemExit('Falta AI33_API_KEY en el entorno o .env de la skill. No la pegues en el chat.')
    return value


def api(path, data=None, content_type=None):
    headers = {'xi-api-key': clave(), 'Accept': 'application/json'}
    if content_type:
        headers['Content-Type'] = content_type
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.load(response)
    except urllib.error.HTTPError as e:
        # No imprimir cabeceras ni cuerpos arbitrarios que puedan contener secretos.
        raise RuntimeError(f'AI33 HTTP {e.code}; conserva la tarea y revisa la cuenta.') from None
    if result.get('success') is False:
        raise RuntimeError('AI33 devolvió success=false; revisa el estado en tu cuenta.')
    return result


def saldo():
    return api('/v1/credits')['credits']


def guardar(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def multipart(fields):
    boundary = 'ai33-' + uuid.uuid4().hex
    data = b''
    for key, value in fields.items():
        data += (f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n').encode('utf-8')
    return data + f'--{boundary}--\r\n'.encode(), 'multipart/form-data; boundary=' + boundary


def generar(text, voice_id, speed, record_path, timeout=1800):
    if not voice_id.startswith(('elevenlabs_', 'minimax_', 'clone_', 'edge_', 'kokoro_', 'vbee_', 'fishaudio_')):
        raise SystemExit('Configura voz_id con el ID completo devuelto por /v3/voices de AI33.')
    speed = float(speed)
    if not 0.5 <= speed <= 1.5:
        raise SystemExit('ai33_speed debe estar entre 0.5 y 1.5.')
    fields = dict(text=text, voice_id=voice_id, speed=str(speed), with_transcript='false')
    digest = hashlib.sha256(json.dumps(fields, sort_keys=True).encode()).hexdigest()
    # Cada contenido conserva su propia tarea: cambiar y volver no duplica el POST.
    path = Path(record_path).with_name(Path(record_path).stem + '-' + digest + '.json')
    audio = path.with_suffix('.mp3')
    lock = path.with_suffix('.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError('Ya hay una operación para esta toma. Comprueba el proceso antes de quitar su .lock.') from None
    os.close(fd)
    try:
        record = json.loads(path.read_text()) if path.exists() else {}
        if record.get('status') == 'done' and audio.exists() and audio.stat().st_size > 1000:
            return audio.read_bytes()
        if record.get('status') == 'error':
            raise RuntimeError('La tarea AI33 registrada falló; revisa su ID en la cuenta antes de crear otra.')
        if not record.get('task_id'):
            if record.get('status') == 'submission_unknown':
                raise RuntimeError('POST previo de resultado desconocido. Recupera task_id desde la cuenta y añádelo al registro antes de continuar.')
            body, content_type = multipart(fields)
            # Antes del POST: una interrupción no debe causar doble cobro al reejecutar.
            record = dict(status='submission_unknown', sha256=digest, voice_id=voice_id, speed=speed, caracteres=len(text))
            clave()  # Fallar antes de dejar una marca ambigua si falta la clave.
            guardar(path, record)
            result = api('/v3/text-to-speech', body, content_type)
            task_id = result.get('task_id')
            if not task_id:
                raise RuntimeError('AI33 no devolvió task_id. No reenviar el POST; revisar la cuenta.')
            record.update(task_id=task_id, status='doing')
            guardar(path, record)
        deadline = time.monotonic() + timeout
        while True:
            task = api('/v1/task/' + urllib.parse.quote(str(record['task_id']), safe=''))
            record.update(status=task.get('status', 'doing'), credit_cost=task.get('credit_cost'))
            guardar(path, record)
            if record['status'] == 'error':
                raise RuntimeError('La tarea AI33 terminó en error; consulta su ID en la cuenta. No se reintentó el POST.')
            if record['status'] == 'done':
                url = task.get('metadata', {}).get('audio_url')
                if not url or urllib.parse.urlparse(url).scheme != 'https':
                    raise RuntimeError('Tarea terminada sin audio_url HTTPS. Conserva task_id y revisa la cuenta.')
                # Descarga sin xi-api-key: la URL puede pertenecer a un CDN.
                with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as response:
                    data = response.read()
                if len(data) <= 1000:
                    raise RuntimeError('Audio vacío o demasiado pequeño; conserva la tarea para reanudar la descarga.')
                temp = audio.with_suffix('.part')
                temp.write_bytes(data)
                temp.replace(audio)
                print('AI33: tarea terminada; créditos reales:', record.get('credit_cost'))
                return data
            if time.monotonic() >= deadline:
                raise TimeoutError('AI33 sigue procesando. Reejecuta para reanudar el mismo task_id, sin otro POST.')
            time.sleep(5)
    finally:
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comando', choices=['saldo', 'voces'])
    parser.add_argument('--provider', choices=['elevenlabs', 'minimax', 'clone', 'edge', 'kokoro', 'vbee', 'fishaudio'])
    args = parser.parse_args()
    if args.comando == 'saldo':
        print('Créditos AI33:', saldo())
    else:
        if not args.provider:
            parser.error('voces requiere --provider')
        page = 1
        while True:
            result = api('/v3/voices?' + urllib.parse.urlencode(dict(provider=args.provider, page=page, page_size=100)))
            for voice in result.get('data', []):
                print(json.dumps({k: voice.get(k) for k in ['voice_id', 'name', 'language']}, ensure_ascii=False))
            if not result.get('pagination', {}).get('has_more'):
                break
            page += 1


if __name__ == '__main__':
    main()
