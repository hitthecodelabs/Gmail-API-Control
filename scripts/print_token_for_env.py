import argparse
import base64

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token", default="token.json", help="Ruta al token.json/token_s.json")
    args = p.parse_args()

    with open(args.token, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    print(b64)

if __name__ == "__main__":
    main()
