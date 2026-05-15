
from src.extract import extract
from src.transform import transform
from src.load import load

path = ""

def main():
    data = extract(path)
    processed = transform(data)
    load(processed)

if __name__ == "__main__": 
    main()
