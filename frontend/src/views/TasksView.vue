<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import TasksComponent from '@/components/TaskComponent.vue'
import CreateTaskComponent from '@/components/CreateTaskComponent.vue'

const tasks = ref([])
const error = ref('')

async function getTasks() {
    try {
        const path = 'http://localhost:5000/tasks'
        const res = await axios.get(path)
        tasks.value = res.data?.tasks
    } catch (err) {
        console.error(err)
    }
}

async function removeTask(taskId) {
    console.log(`taskId = `, taskId)
    const path = `http://localhost:5000/tasks/${taskId}`
    try {
        const res = await axios.delete(path)
        console.log(res.data)
        if (res.data?.status === 'success') {
            tasks.value = tasks.value.filter(
                (task) => task.id !== Number(taskId)
            )
        }
    } catch (err) {
        console.error(err)
    }
}

function addTask(title, description) {
    tasks.value.push({ id: 50, title: title, description: description })
}

async function updateTask(event) {
    error.value = ''
    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    if (!title || !description) {
        error.value = 'One of title or description is missing!'
    } else {
        tasks.value.push({ id: 40, title: title, description: description })
    }
}

onMounted(() => {
    getTasks()
})
</script>

<template>
    <div class="task_manager_container">
        <h1>Task Manager</h1>
        <CreateTaskComponent @add-task="addTask" />
        <TasksComponent
            v-for="task in tasks"
            :key="task.id"
            v-bind="task"
            @remove-task="removeTask"
        />
    </div>
</template>

<style>
.task_manager_container {
    display: flex;
    flex-direction: column;
    text-align: center;
    gap: 16px;
    margin: 16px;
}

.task_header {
    display: flex;
}
</style>
