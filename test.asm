.model small
.data
i db  1 dup(?)
j db  1 dup(?)
temp1 db  1 dup(?)
temp2 db  1 dup(?)
temp3 db  1 dup(?)
a db  2, 3, 4, 1, 5
.stack
.code
main:
mov ax,@data
mov ds,ax
mov al,4
mov ah,0
push ax
pop ax
mov i,al
label_0:
mov al,i
mov bl,0
cmp al,bl
jl label_1
mov al,0
mov ah,0
push ax
pop ax
mov j,al
label_2:
mov al,j
mov bl,i
cmp al,bl
jge label_3
mov cl,j
mov ch,0
mov di,cx
mov al,a[di]
mov ah,0
push ax
pop ax
mov temp1,al
mov al,1
mov bl,1
mul bl
mov ah,0
push ax
mov al,1
mov bl,1
mul bl
mov ah,0
push ax
pop ax
pop bx
add al,bl
mov ah,0
push ax
pop ax
mov bl,1
sub al,bl
mov ah,0
push ax
mov al,j
pop bx
add al,bl
mov ah,0
push ax
pop ax
mov temp3,al
mov cl,temp3
mov ch,0
mov di,cx
mov al,a[di]
mov ah,0
push ax
pop ax
mov temp2,al
mov al,temp1
mov bl,temp2
cmp al,bl
jle label_4
mov al,temp1
mov ah,0
push ax
pop ax
mov cl,temp3
mov ch,0
mov di,cx
mov a[di],al
mov al,temp2
mov ah,0
push ax
pop ax
mov cl,j
mov ch,0
mov di,cx
mov a[di],al
jmp label_5
label_4:
label_5:
inc j
jmp label_2
label_3:
dec i
jmp label_0
label_1:
mov al,0
mov ah,0
push ax
pop ax
mov i,al
label_8:
mov al,i
mov bl,5
cmp al,bl
jge label_9
mov cl,i
mov ch,0
mov di,cx
mov al,a[di]
mov ah,0
push ax
pop ax
mov ah,0
call printn
mov al,i
mov bl,1
add al,bl
mov ah,0
push ax
pop ax
mov i,al
jmp label_8
label_9:
mov al,0
mov ah,0
push ax
pop ax
mov ah,0
push ax
mov ah,4ch
int 21h
printn proc near
mov bx,10
mov cx,0
yazhan: mov dx,0
div bx
push dx
inc cx
cmp ax,0
jz chuzhan
jmp yazhan
chuzhan: pop dx
add dl,30h
mov ah,2
int 21h
loop chuzhan
ret
printn endp
END main
