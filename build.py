import os
from xml.etree.ElementTree import ElementTree

locl_table_numbers = ('119', '120', '121', '122', '123')

weights = [
    'Bold',
    'ExtraLight',
    'Heavy',
    'Light',
    'Medium',
    'Regular',
    'SemiBold',
]

for weight in weights:
    file = 'SourceHanSerifK-' + weight

    os.system(f'wget -nc https://github.com/adobe-fonts/source-han-serif/raw/55303c3/OTF/Korean/{file}.otf')
    os.system(f'ttx -o {file}.xml {file}.otf')

    tree = ElementTree()
    tree.parse(f'{file}.xml')

    # locate to `<ScriptTag value="hani"/>`
    node = tree.find('GSUB').find('ScriptList').findall('ScriptRecord')[4]
    assert node.get('index') == '4'
    assert node.find('ScriptTag').get('value') == 'hani'
    for script in node.find('Script'):
        for lang in script:
            for feature_index in lang.findall('FeatureIndex'):
                if feature_index.get('value') in locl_table_numbers:
                    print('Removed feature index ' + feature_index.get('value'))
                    lang.remove(feature_index)

    tree.write(f'{file}.2.xml')

    with open(f'{file}.2.xml') as f:
        s = f.read()
        s = '<?xml version="1.0" encoding="UTF-8"?>' + s
    with open(f'{file}.2.xml', 'w') as f:
        f.write(s)

    os.system(f'ttx -o {file}.2.otf {file}.2.xml')
