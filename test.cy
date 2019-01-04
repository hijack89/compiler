#冒泡排序,cython语言示例程序
int cython(){
    int i,j,temp1,temp2,temp3,a[5]{2,3,4,1,5}
    for(i=4;i>=0;i--)
    {
        for(j=0;j<i;j++)
        {
            temp1=a[j]
            temp3=j+(1*1+1*1-1)
            temp2=a[temp3]
            if(temp1>temp2)
            {
                a[temp3]=temp1
                a[j]=temp2
            }
        }
    }
    i=0
    while(i<5){
        print a[i]
        i=i+1
    }
    return 0
}