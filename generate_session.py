import sys
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
import asyncio
from pyrogram import Client

print(r"""
=============================================================
   亗 PYROFORK STRING SESSION GENERATOR 亗
=============================================================
Get your API_ID and API_HASH from https://my.telegram.org
""")

async def generate():
    api_id_input = input("Enter API_ID: ").strip()
    if not api_id_input.isdigit():
        print("❌ API_ID must be numbers only!")
        return
    api_id = int(api_id_input)
    api_hash = input("Enter API_HASH: ").strip()

    print("\nConnecting to Telegram servers...")
    async with Client(name=":memory:", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
        session_string = await app.export_session_string()
        me = await app.get_me()

        print("\n" + "=" * 60)
        print(f"✅ SUCCESS! Logged in as: {me.first_name} (@{me.username or 'No Username'})")
        print("=" * 60)
        print("\n👇 YOUR STRING SESSION (Copy this entire string):")
        print(session_string)
        print("\n" + "=" * 60)
        print("⚠️ Keep this session private! Anyone with this string can access your Telegram.")

        # Ask to save to .env
        save_choice = input("\nDo you want to save this to your .env file directly? (y/n): ").strip().lower()
        if save_choice == 'y':
            lines = []
            try:
                with open(".env", "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                pass

            new_lines = []
            session_set = False
            id_set = False
            hash_set = False
            for line in lines:
                if line.startswith("STRING_SESSION="):
                    new_lines.append(f"STRING_SESSION={session_string}\n")
                    session_set = True
                elif line.startswith("API_ID="):
                    new_lines.append(f"API_ID={api_id}\n")
                    id_set = True
                elif line.startswith("API_HASH="):
                    new_lines.append(f"API_HASH={api_hash}\n")
                    hash_set = True
                else:
                    new_lines.append(line)

            if not session_set:
                new_lines.append(f"STRING_SESSION={session_string}\n")
            if not id_set:
                new_lines.append(f"API_ID={api_id}\n")
            if not hash_set:
                new_lines.append(f"API_HASH={api_hash}\n")

            with open(".env", "w") as f:
                f.writelines(new_lines)
            print("✅ Saved credentials to .env file!")

if __name__ == "__main__":
    asyncio.run(generate())
