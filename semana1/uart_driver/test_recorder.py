
from recorder import Recorder, JsonLineRecorder

def test_recorder_base():

    recorder = Recorder()

    assert hasattr(recorder, "guardar")

def test_json_line_recorder(tmp_path):

    archivo = tmp_path / "datos.jsonl"

    recorder = JsonLineRecorder(archivo)

    datos = {
        "temperatura": 25,
        "humedad": 60
    }

    resultado = recorder.guardar(datos)

    assert resultado == {
        "mensaje": "Datos guardados en JSON-lines"
    }

    contenido = archivo.read_text()

    assert '"temperatura": 25' in contenido


def test_json_line_multiple_records(tmp_path):

    archivo = tmp_path / "datos.jsonl"

    recorder = JsonLineRecorder(archivo)

    recorder.guardar({"temperatura": 20})
    recorder.guardar({"temperatura": 21})

    lineas = archivo.read_text().splitlines()

    assert len(lineas) == 2