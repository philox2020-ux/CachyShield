#!/bin/fish
if test (count $argv) -lt 1
    echo "❌ Usage: ./inject.sh [command_name]"
    exit 1
end

set cmd $argv[1]
set cmd_path (which $cmd 2>/dev/null)

if not test -f "$cmd_path"
    echo "❌ Command \"$cmd\" not found on your host machine."
    exit 1
end

echo "🔍 Injecting \"$cmd\" from $cmd_path into CachyShield..."

# Create necessary directories inside the jail
mkdir -p "jail"(dirname $cmd_path)
cp $cmd_path "jail"$cmd_path

# Automatically find and copy all shared library dependencies
for lib in (ldd $cmd_path | grep -o '/[^ ]*lib[^ ]*')
    if test -f $lib
        mkdir -p "jail"(dirname $lib)
        cp $lib "jail"$lib 2>/dev/null
    end
end

echo "✅ Successfully injected \"$cmd\" and all its library dependencies!"
