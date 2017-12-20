package main 

import (
	"fmt"
)

func main(){

	s := "hello world"
	fmt.Println(s)
	fmt.Println(s[3])
	if s[3]=='l'{
		fmt.Printf("equal\n")
	} else {
		fmt.Printf("not equal\n")
	}

	for _,x := range []rune(s){
		fmt.Printf("char:%c\n",x)
	}
}