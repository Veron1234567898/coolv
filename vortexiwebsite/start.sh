#!/bin/bash
cat <<'EOF'
 __     __                       __                          __ 
/  |   /  |                     /  |                        /  |
$$ |   $$ | ______    ______   _$$ |_     ______   __    __ $$/ 
$$ |   $$ |/      \  /      \ / $$   |   /      \ /  \  /  |/  |
$$  \ /$$//$$$$$$  |/$$$$$$  |$$$$$$/   /$$$$$$  |$$  \/$$/ $$ |
 $$  /$$/ $$ |  $$ |$$ |  $$/   $$ | __ $$    $$ | $$  $$<  $$ |
  $$ $$/  $$ \__$$ |$$ |        $$ |/  |$$$$$$$$/  /$$$$  \ $$ |
   $$$/   $$    $$/ $$ |        $$  $$/ $$       |/$$/ $$  |$$ |
    $/     $$$$$$/  $$/          $$$$/   $$$$$$$/ $$/   $$/ $$/ 


EOF
echo "BUILD_HASH = \"$(python3 -c 'import uuid, hashlib; print(hashlib.sha256(uuid.uuid4().bytes).hexdigest()[:8])')\"" > app/build_version.py # random string each start to avoid cloudflare caching our css :p
echo "Version - $(grep -oP '(?<=BUILD_HASH = ")[a-f0-9]+' app/build_version.py) (prod)"
echo "Running Vortexi OSS at $(date)"
gunicorn -b 0.0.0.0:3003 --preload --workers=8 --threads=20 "app:create_app()"
