rm -rf build dist
rm setup.py
py2applet --make-setup Habitus.py
python setup.py py2app --iconfile images/icon.icns
mkdir dist/Habitus.app/Contents/Resources/images
cp images/icon-bw.png dist/Habitus.app/Contents/Resources/images/icon-bw.png
mv ./dist/Habitus.app /Applications
