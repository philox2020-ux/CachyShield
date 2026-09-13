#!/bin/fish
echo "🧹 Wiping old sandbox folder..."
sudo rm -rf jail
mkdir -p jail/bin jail/lib jail/lib64 jail/usr/bin jail/usr/lib/python3.14/lib-dynload jail/usr/share/terminfo/x jail/etc jail/proc jail/dev

echo "🧱 Rebuilding core system files..."
# Copy the basic terminal tools
cp /bin/bash /bin/ls /bin/echo /bin/mkdir jail/bin/
cp -r /usr/share/terminfo/x/* jail/usr/share/terminfo/x/
echo "export PATH=/bin:/usr/bin" > jail/etc/profile

# Create the essential /dev/null device inside the sandbox
sudo mknod -m 666 jail/dev/null c 1 3

echo "🧬 Copying core system libraries..."
for bin in bash ls echo mkdir
    for lib in (ldd /bin/$bin | grep -o '/[^ ]*lib[^ ]*')
        if test -f $lib
            mkdir -p "jail"(dirname $lib)
            cp $lib "jail"$lib 2>/dev/null
        end
    end
end
cp /usr/lib/libcap.so.2 jail/usr/lib/

echo "🐍 Injecting full Python 3.14 runtime engine..."
cp /usr/bin/python3 jail/usr/bin/
ln -s /usr/bin/python3 jail/usr/bin/python
for lib in (ldd /usr/bin/python3 | grep -o '/[^ ]*lib[^ ]*')
    if test -f $lib
        mkdir -p "jail"(dirname $lib)
        cp $lib "jail"$lib 2>/dev/null
    end
end

# Copy Python files while carefully avoiding system folders
cp -r /usr/lib/python3.14/* jail/usr/lib/python3.14/ 2>/dev/null

echo "✨ CachyShield Reset Complete! Everything is fresh and perfect."
