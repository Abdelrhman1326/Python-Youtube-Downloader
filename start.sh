echo "Setting up Python Youtube Downloader..."

if [ -d ".venv/bin/Activate" ]; then
    echo "Cleaning up accidental 'Activate' folder..."
    rm -r .venv/bin/Activate
fi

if [ ! -d ".venv" ]; then
    echo "Creating fresh virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing/verifying requirements..."
pip install -r requirements.txt

echo "Starting Downloader.py..."
echo "-----------------------------------"
python3 Downloader.py
echo "-----------------------------------"

deactivate
echo "Downloader closed and environment deactivated."
