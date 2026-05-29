#!/bin/bash
# Fix SMRITI page folder names: dash → underscore (Frappe scrub() requirement)
PAGE_DIR=/home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/page

for dir in smriti-backup smriti-barcode smriti-billing smriti-desk smriti-inventory smriti-loyalty smriti-purchase smriti-reports smriti-shift; do
    newdir="${dir//-/_}"
    oldpath="$PAGE_DIR/$dir"
    newpath="$PAGE_DIR/$newdir"

    if [ -d "$oldpath" ]; then
        # Copy dir with new name
        cp -r "$oldpath" "$newpath"

        # Rename files inside: smriti-X.ext -> smriti_X.ext
        for f in "$newpath"/*; do
            base=$(basename "$f")
            newbase="${base//-/_}"
            if [ "$base" != "$newbase" ]; then
                mv "$f" "$newpath/$newbase"
                echo "  file: $base -> $newbase"
            fi
        done

        # Remove old dash-named directory
        rm -rf "$oldpath"
        echo "Renamed dir: $dir -> $newdir"
    else
        echo "Skipping (not found): $dir"
    fi
done

echo ""
echo "Final page directory listing:"
ls "$PAGE_DIR"
