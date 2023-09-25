<script setup>
defineProps(['id', 'title', 'description'])
</script>

<template>
    <div class="task_container">
        <span class="title">{{ title }}</span>
        <span class="vertical_divider"></span>
        <div class="description_container">
            <p>
                {{ description }}
            </p>
        </div>
        <span class="vertical_divider"></span>
        <div class="btn_container">
            <button class="btn">Update</button>
            <button
                class="btn btn-danger"
                @click.prevent="$emit('removeTask', id)"
            >
                Delete
            </button>
        </div>
    </div>
</template>

<style>
.task_container {
    display: flex;
    background-color: lightgray;
    justify-content: space-between;
    border-radius: 16px;
    color: black;
}

.title {
    min-width: 150px;
    max-width: 280px;
    width: 20%;
    align-self: center;
    margin: 8px;
}

.description_container {
    width: 70%;
    align-self: center;
    padding: 0 8px;
    margin: 8px;
}

@media screen and (min-width: 800px) {
    .btn_container {
        min-width: 200px;
    }
}

.btn_container {
    width: min-content;
    align-self: center;
}

.btn {
    padding: 12px 16px;
    margin: 8px 8px;
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;
}

.btn-danger {
    background-color: rgba(238, 0, 0, 0.82);
    color: white;

    &:hover {
        background-color: #c70000;
    }
}

.vertical_divider {
    width: 1px;
    border-right: 1px solid white;
}
</style>
