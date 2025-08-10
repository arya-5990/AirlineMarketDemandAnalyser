# Airline Market Demand Analyzer - Launch Script
Write-Host "Starting Airline Market Demand Analyzer..." -ForegroundColor Green
Write-Host ""
Write-Host "The application will open in your default web browser." -ForegroundColor Yellow
Write-Host "If it doesn't open automatically, go to: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the application." -ForegroundColor Cyan
Write-Host ""

# Run the Streamlit application
python -m streamlit run main.py 