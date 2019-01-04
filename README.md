小型自制cython编译器
=========================

overview
------------------------
1.包括词法分析、语法分析、生成汇编

2.目标语言是Intel x86的16位汇编代码

3.语言结合了c和python的特点

4.语言以换行作为每句程序的结束

5.变量类型只实现了int型

基本句型
------------------------
1.声明语句

2.赋值语句

3.控制流语句（for、while、if-else）

4.输入语句

5.输出语句

6.返回语句


用法(假设源文件为source.c)
------------------------
* 帮助：

    `python compiler.py -h`

* 查看词法分析结果：

    `python compiler.py source.c -l`

* 查看语法树：

    `python compiler.py source.c -p`

* 生成汇编：

    `python compiler.py source.c -a`

* 汇编asm程序：

    `ml /c source.asm`

* 链接obj程序：
    `link16 source.obj`



注意：
------------------------
由于采用了16位Intel汇编语言，所以需要使用16位链接器进行obj文件的链接；
且可执行程序需要在dosbox软件或32位windows中运行



TODO:
------------------------
实现了基本的语法句型，函数的声明和调用基本没有实现（只实现了主函数声明）
还有其他语法句型待完善


Test Environment
------------------------
* windows 7 x86
* Python version: 2.7


