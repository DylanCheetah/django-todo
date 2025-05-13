document.addEventListener("DOMContentLoaded", () => {
    // Globals
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let todoLists = null;

    // Functions
    function loadTodoLists(url) {
        // Show busy indicator
        document.querySelector("#todoListSpinner").classList.remove("d-none");

        // Fetch todo lists from server
        fetch(url, {
                credentials: "same-origin",
                cache: "no-store"
        })
        .then((response) => response.json())
        .then((payload) => {
            // Store payload
            todoLists = payload;

            // Clear previous page of todo lists
            const todoListView = document.querySelector("#todoListView");

            while(todoListView.childElementCount) {
                todoListView.removeChild(todoListView.firstChild);
            }

            // Display todo lists
            todoLists.results.forEach((todoList) => {
                // Create row
                let row = document.createElement("div");
                row.classList.add("row");

                // Create todo list card
                let todoListCard = document.createElement("div");
                todoListCard.classList.add("col", "m-1", "card", "bg-light");
                row.appendChild(todoListCard);

                // Create card body
                let cardBody = document.createElement("div");
                cardBody.classList.add("card-body", "row");
                cardBody.id = `todoList${todoList.id}`;
                todoListCard.appendChild(cardBody);

                let cardTitle = document.createElement("h5");
                cardTitle.classList.add("col-9", "m-1", "card-title");
                cardTitle.id = `todoListTitle${todoList.id}`;
                cardTitle.innerText = todoList.name;
                cardBody.appendChild(cardTitle);

                let cardEditBtn = document.createElement("button");
                cardEditBtn.classList.add("col-1", "m-1", "btn", "btn-warning");
                cardEditBtn.innerText = "Edit";
                cardEditBtn.dataset.id = todoList.id;
                cardEditBtn.addEventListener("click", (evt) => editTodoList(evt.target.dataset.id));
                cardBody.appendChild(cardEditBtn);

                let cardDeleteBtn = document.createElement("button");
                cardDeleteBtn.classList.add("col-1", "m-1", "btn", "btn-danger");
                cardDeleteBtn.innerText = "Delete";
                cardDeleteBtn.dataset.id = todoList.id;
                cardDeleteBtn.addEventListener("click", (evt) => deleteTodoList(evt.target.dataset.id));
                cardBody.appendChild(cardDeleteBtn);

                // Create editable card body
                let cardBody2 = document.createElement("div");
                cardBody2.classList.add("card-body", "row", "d-none");
                cardBody2.id = `editableTodoList${todoList.id}`;
                todoListCard.append(cardBody2);

                let cardTitleInput = document.createElement("input");
                cardTitleInput.classList.add("col-9", "m-1");
                cardTitleInput.id = `todoListTitleInput${todoList.id}`;
                cardTitleInput.type = "text";
                cardTitleInput.value = todoList.name;
                cardBody2.appendChild(cardTitleInput);

                let cardConfirmEditBtn = document.createElement("button");
                cardConfirmEditBtn.classList.add("col-1", "m-1", "btn", "btn-success");
                cardConfirmEditBtn.innerText = "Confirm";
                cardConfirmEditBtn.dataset.id = todoList.id;
                cardConfirmEditBtn.addEventListener("click", (evt) => confirmEditTodoList(evt.target.dataset.id));
                cardBody2.appendChild(cardConfirmEditBtn);

                let cardCancelEditBtn = document.createElement("button");
                cardCancelEditBtn.classList.add("col-1", "m-1", "btn", "btn-danger");
                cardCancelEditBtn.innerText = "Cancel";
                cardCancelEditBtn.dataset.id = todoList.id;
                cardCancelEditBtn.addEventListener("click", (evt) => cancelEditTodoList(evt.target.dataset.id));
                cardBody2.appendChild(cardCancelEditBtn);

                // Add row to todo list view
                todoListView.appendChild(row);
            });

            // Update page turner
            // TODO

            // Hide busy indicator
            document.querySelector("#todoListSpinner").classList.add("d-none");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function addTodoList() {
        const nameInput = document.querySelector("#todoListNameInput");

        fetch("/api/v1/todo-lists/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                name: nameInput.value
            }),
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 201) {
                alert("Failed to add todo list.");
                return;
            }

            // Clear todo list name input
            nameInput.value = "";

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function editTodoList(id) {
        // Hide read-only todo list and show editable todo list
        document.querySelector(`#todoList${id}`).classList.add("d-none");
        document.querySelector(`#editableTodoList${id}`).classList.remove("d-none");
    }

    
    function deleteTodoList(id) {
        fetch(`/api/v1/todo-lists/${id}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken
            },
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 204) {
                alert("Failed to delete todo list.");
                return;
            }

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function cancelEditTodoList(id) {
        // Sync todo list title input with todo list title
        document.querySelector(`#todoListTitleInput${id}`).value = document.querySelector(`#todoListTitle${id}`).innerText;

        // Hide editable todo list and show read-only todo list
        document.querySelector(`#editableTodoList${id}`).classList.add("d-none");
        document.querySelector(`#todoList${id}`).classList.remove("d-none");
    }


    function confirmEditTodoList(id) {
        // Get new todo list name
        const todoListTitleInput = document.querySelector(`#todoListTitleInput${id}`);

        // Update todo list name
        fetch(`/api/v1/todo-lists/${id}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                name: todoListTitleInput.value
            }),
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 200) {
                alert("Failed to update todo list.");
                return;
            }

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function previousPage() {
        if(!todoLists.previous) {
            return;
        }

        loadTodoLists(todoLists.previous);
    }


    function nextPage() {
        if(!todoLists.next) {
            return;
        }
        
        loadTodoLists(todoLists.next);
    }

    // Add event listeners
    const addTodoListBtn = document.querySelector("#addTodoListBtn");
    const prevPageBtn = document.querySelector("#prevPageBtn");
    const nextPageBtn = document.querySelector("#nextPageBtn");

    addTodoListBtn.addEventListener("click", addTodoList);
    prevPageBtn.addEventListener("click", previousPage);
    nextPageBtn.addEventListener("click", nextPage);

    // Load first page of todo lists
    loadTodoLists("/api/v1/todo-lists/");
});
