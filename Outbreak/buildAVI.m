% Robert Pienta
clear all
clc
aviobj = avifile('outBreak8.avi','compression','Cinepak', 'fps', 32);
extension = '*.png';
files = dir(extension);
for i=1:size(files, 1)
    [pathstr, name, ext, versn] = fileparts(files(i).name);
    y(i) = str2num(char(name));
end
[B, index] = sort(y,2);
for i=1:size(files, 1)
    i/size(files, 1)
    aviobj = addframe(aviobj,imread(files(index(i)).name));
end
aviobj = close(aviobj);