import pickle
from pathlib import Path
import streamlit_authenticator as str

passwords=["admin","work"]


hashed_passwords=str.Hasher(passwords).generate()

file_path= Path(__file__).parent / "hashed.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)