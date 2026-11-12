from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, HTMLResponse
import zipfile
import io
from processing import denoise_audio

app = FastAPI(
    title="Audio Signal Processing API", 
    description="Engineered for Software Mansion Internship Application"
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <h1>API is running</h1>
    <p>Przejdź do interfejsu testowego: <a href='/docs'><b>/docs</b></a>, aby wgrać plik .wav.</p>
    """

@app.post("/api/v1/process-audio")
async def process_audio_endpoint(file: UploadFile = File(...)):
    # Odczyt pliku wgranego przez użytkownika
    content = await file.read()
    
    # Przekazanie do logiki biznesowej (analitycznej)
    audio_io, plot_io = denoise_audio(content)
    
    # Pakowanie wyników do archiwum ZIP w pamięci RAM
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("cleaned_audio.wav", audio_io.read())
        zip_file.writestr("spectrogram_comparison.png", plot_io.read())
        
    zip_buffer.seek(0)
    
    # Zwrócenie odpowiedzi do klienta
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=processed_results.zip"}
    )