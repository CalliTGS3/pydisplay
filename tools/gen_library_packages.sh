#!/bin/env bash
# Copy packages to the micropython-lib directory
# Install example:  mip.install("displaysys", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
# Resolves to:  https://pydevices.github.io/micropython-lib/mip/PyDevices/package/6/displaysys/latest.json
# Repo URL:  https://github.com/PyDevices/micropython-lib/blob/gh-pages/mip/PyDevices/package/6/displaysys/latest.json

VERSION=0.1.6
DESCRIPTION_PREFIX="PyDisplay"
AUTHOR="Brad Barnett <contact@pydevices.com>"
LICENSE="MIT"

BASENAME=pydisplay
DEST_REPO=~/gh/micropython-lib
SOURCE_REPO=~/gh/$BASENAME
SOURCE_DIR=$SOURCE_REPO/src
DEST_DIR=$DEST_REPO/micropython/$BASENAME
BUNDLE_MANIFEST=$DEST_DIR/$BASENAME-bundle/manifest.py
PYPI_DIR=$SOURCE_REPO/wheels
README_FULL_PATH=$SOURCE_REPO/README.md

DISPLAY_SOURCE_DIR=$SOURCE_REPO/drivers/display
TOUCH_SOURCE_DIR=$SOURCE_REPO/drivers/touch
DISPLAY_DEST_DIR=$DEST_REPO/micropython/drivers/display
TOUCH_DEST_DIR=$DEST_REPO/micropython/drivers/touch

set -e

# Create the bundle manifest
mkdir -p $DEST_DIR/$BASENAME-bundle
cat <<EOF > $BUNDLE_MANIFEST
metadata(
    description="$DESCRIPTION_PREFIX bundle",
    version="$VERSION",
    author="$AUTHOR",
    license="$LICENSE",
    pypi_publish="$BASENAME-bundle",
)
EOF

# Copy all the directories in $SOURCE_DIR/lib except displaysys to $DEST_DIR/$package
# Copy any example files starting with the package name to $DEST_DIR/$package/examples
for package_dir in "$SOURCE_DIR/lib"/*; do
    package=$(basename $package_dir)
    if [ -d $package_dir ] && [ $(basename $package) != "displaysys" ]; then
        mkdir -p $DEST_DIR/$package/examples
        cp -r $package_dir $DEST_DIR/$package/
        cp $SOURCE_DIR/examples/$package*.py $DEST_DIR/$package/examples/
        # write the following text to $DEST_DIR/$package/manifest.py
        cat <<EOF > $DEST_DIR/$package/manifest.py
metadata(
    description="$DESCRIPTION_PREFIX $package",
    version="$VERSION",
    author="$AUTHOR",
    license="$LICENSE",
    pypi_publish="$BASENAME-$package",
)
package("$package")
EOF
        echo "require(\"$package\")" >> $BUNDLE_MANIFEST
        cp $README_FULL_PATH $DEST_DIR/$package/README.md
        ./tools/makepyproject.py --output $PYPI_DIR/$package $DEST_DIR/$package/manifest.py
        pushd $PYPI_DIR/$package
        hatch build
        popd
    fi
done

# Copy the children of displaysys to $DEST_DIR/displaysys/$package/displaysys
for module in "$SOURCE_DIR/lib/displaysys"/*; do
    if [[ $(basename $module) == __init__.py ]]; then
        package=displaysys
    else
        package_dir=$(basename $module .py)
        package=displaysys-$package_dir
    fi
    mkdir -p $DEST_DIR/displaysys/$package/displaysys
    cp -r $module $DEST_DIR/displaysys/$package/displaysys/
    mkdir -p $DEST_DIR/displaysys/$package/examples
    if [[ $package == displaysys ]]; then
        cat <<EOF > $DEST_DIR/displaysys/$package/manifest.py
metadata(
    description="$DESCRIPTION_PREFIX $package",
    version="$VERSION",
    author="$AUTHOR",
    license="$LICENSE",
    pypi_publish="$BASENAME-$package",
)
package("displaysys")
EOF
        echo "require(\"$package\")" >> $BUNDLE_MANIFEST
        cp $README_FULL_PATH $DEST_DIR/displaysys/$package/$package/README.md
        ./tools/makepyproject.py --output $PYPI_DIR/$package  $DEST_DIR/displaysys/$package/manifest.py
        pushd $PYPI_DIR/$package
        hatch build
        popd
        cp $SOURCE_DIR/examples/$package*.py $DEST_DIR/displaysys/$package/examples/
    else
        cat <<EOF > $DEST_DIR/displaysys/$package/manifest.py
metadata(
    description="$DESCRIPTION_PREFIX $package",
    version="$VERSION",
    author="$AUTHOR",
    license="$LICENSE",
    pypi_publish="$BASENAME-$package",
)
require("displaysys")
package("displaysys")
EOF
        echo "require(\"$package\")" >> $BUNDLE_MANIFEST
        # TODO:  After publishing displaysys, uncomment the following 4 lines
        # cp $README_FULL_PATH $DEST_DIR/displaysys/$package/README.md
        # ./tools/makepyproject.py --output $PYPI_DIR/$package $DEST_DIR/displaysys/$package/manifest.py
        # pushd $PYPI_DIR/$package
        # hatch build
        # popd
        if [[ $package == displaysys-busdisplay ]]; then
            cp $SOURCE_DIR/../board_configs/busdisplay/i80/wt32sc01-plus/board_config.py $DEST_DIR/displaysys/$package/examples/
        else
            if [[ $package == displaysys-fbdisplay ]]; then
                cp $SOURCE_DIR/../board_configs/fbdisplay/qualia_tl040hds20/board_config.py $DEST_DIR/displaysys/$package/examples/
            else
                cp $SOURCE_DIR/../board_configs/$package_dir/board_config.py $DEST_DIR/displaysys/$package/examples/
            fi
        fi
    fi
done

# Create a package for the display drivers
mkdir -p $DISPLAY_DEST_DIR
for display_driver in "$DISPLAY_SOURCE_DIR"/*.py; do
    if [ -d $display_driver ]; then
        continue
    fi
    package=$(basename $display_driver .py)
    mkdir -p $DISPLAY_DEST_DIR/$package
    cp -r $display_driver $DISPLAY_DEST_DIR/$package/
    cat <<EOF > $DISPLAY_DEST_DIR/$package/manifest.py
metadata(
    description="$DESCRIPTION_PREFIX $package display driver",
    version="$VERSION",
)
module("$package.py", opt=3)
EOF
done

# Create a package for the touch drivers
mkdir -p $TOUCH_DEST_DIR
for touch_driver in "$TOUCH_SOURCE_DIR"/*.py; do
    package=$(basename $touch_driver .py)
    mkdir -p $TOUCH_DEST_DIR/$package
    cp -r $touch_driver $TOUCH_DEST_DIR/$package/
    cat <<EOF > $TOUCH_DEST_DIR/$package/manifest.py
metadata(
    description="$DESCRIPTION_PREFIX $package touch driver",
    version="$VERSION",
)
module("$package.py", opt=3)
EOF
done

echo "To commit changes now, enter your git commit message, otherwise, press enter."
echo "The commit should be in the format:  '$BASENAME:  At least two words and a period.'"
read -p "Enter your git commit message: " commit_message
if [ -n "$commit_message" ]; then
    git -C $DEST_REPO add .
    git -C $DEST_REPO commit -s -m "$commit_message"
    git -C $DEST_REPO push
fi
