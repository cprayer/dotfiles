set t 'snow.colortemplate'
python template-generator.py > $t
vim -c 'Colortemplate! ~/Documents/code/vim/snow' $t -c 'qa!'

for f in ../shell/*.sh
    sed -i '6,23s%"#\(..\)\(..\)\(..\)%"\1/\2/\3%' $f
    sed -i '67,73s/#//' $f
end

for f in ../shell/*.fish
    sed -i 's/ #/ /' $f
end

sed -i '/Last Updated/d' ../colors/snow.vim

for f in ../**
    sed -i -e :a -e '/^\n*$/{$d;N;};/\n$/ba' $f 2>/dev/null
end
