#!/data/data/com.termux/files/usr/bin/bash
# Termux Android 1-Click Installer for Premium Userbot

echo "================================================="
echo "   亗 Premium Userbot Termux Installer 亗"
echo "================================================="

pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git clang libjpeg-turbo libcrypt ndk-sysroot zlib

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "================================================="
echo " Installation Complete!"
echo " 1. Run 'python generate_session.py' to login"
echo " 2. Run 'python main.py' to start your bot!"
echo "================================================="
