var todoTemplate = function (todo) {
    var t = `
    <div class="todo-cell">
        <span>${todo}</span>
    </div>
    `
    /*
    t = """
    <div class="todo-cell">
        <span>{}</span>
    </div>
    """.format(todo)
     */
    return t
}

/*
1. 给 add button 绑定事件
2. 在事件处理函数中，获取 input 的值
3. 用获取的值，组装一个 todo-cell HTML 字符串
4. 插入 todo-list 中
*/

var insertTodo = function (todoCell) {
    var form = document.querySelector('#id-todo-list')
    form.insertAdjacentHTML('beforeEnd', todoCell)
}

var b = e('#id-button-add')
b.addEventListener('click', function () {
    log('click')
    var input = e('#id-input-todo')
    log('html 元素', input)
    log('输入框值', input.value)
    var todo = input.value
    var todoCell = todoTemplate(todo)
    log(todoCell)
    insertTodo(todoCell)
})

ajax('get', '/', '', function(result) {
	console.log(result)
})