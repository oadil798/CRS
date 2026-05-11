# VS Code / Pylance Notes

If VS Code shows:

- `Import "streamlit" could not be resolved`
- `Import "plotly.express" could not be resolved`

it usually means VS Code is not using the Python environment where the project dependencies are installed.

## Fix

From the project folder, run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Then in VS Code:

1. Press `Ctrl + Shift + P`
2. Select `Python: Select Interpreter`
3. Choose `.venv\Scripts\python.exe`
4. Reload VS Code if needed

To confirm installation:

```powershell
python -m pip show streamlit
python -m pip show plotly
```

The CSS file is now pure CSS. The `<style>` wrapper is added inside `src/ui/layout.py`, so VS Code should no longer show CSS errors on `assets/styles/main.css`.
