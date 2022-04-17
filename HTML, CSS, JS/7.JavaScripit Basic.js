// 1. 변수 선언
let a = 1
let first = 'Bob'
let last = 'Lee'
first+last // 'BobLee'
first+' '+last // 'Bob Lee'
first+a // Bob1 -> 문자+숫자를 하면, 숫자를 문자로 바꾼 뒤 수행

// 2. List
let a_list = []
let b_list = [1,2,'hey',3]
b_list.push('헤이') // 리스트에 요소 넣기
b_list // [1, 2, "hey", 3, "헤이"] 를 출력
b_list.length // 리스트의 길이 , 5

// 3. Dict
let a_dict = {}
let b_dict = {'name':'Bob','age':21}
b_dict['name'] // 'Bob'
b_dict['height'] = 180 // 딕셔너리에 키:밸류 넣기

// 4. 함수
function sum(num1, num2) {
	console.log('num1: ', num1, ', num2: ', num2);
	return num1 + num2;
}
sum(4, -1); // 3

// 5. 조건문 if, else if , else
function is_adult(age){
	if(age > 20){
		alert('성인이에요')
	} else if (age > 10) {
		alert('청소년이에요')
	} else {
		alert('10살 이하!')
	}
}

// 6-1. 논리문 - AND
function is_adult(age, sex){
	if(age > 20 && sex == '여'){
		alert('성인 여성')
    }
}

// 6-2. 논리문 - OR
function is_adult(age, sex){
	if (age > 65 || age < 10) {
		alert('탑승하실 수 없습니다')
	}
}

// 7. 반복문
for (let i = 0; i < 100; i++) {
	console.log(i);
}