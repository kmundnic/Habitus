py2applet --make-setup Habitus.py
rm -rf build dist
python setup.py py2app --iconfile images/icon.icns
mkdir dist/Habitus.app/Contents/Resources/images
cp images/icon-bw.png dist/Habitus.app/Contents/Resources/images/icon-bw.png
