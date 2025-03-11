<script setup>
import { ref } from "vue"
import { AllCommunityModule, ModuleRegistry, themeBalham } from 'ag-grid-community'
ModuleRegistry.registerModules([AllCommunityModule])
import { AgGridVue } from "ag-grid-vue3"


const apiUrl = import.meta.env.VITE_API_URL
// AG Grid related data
const autoSizeStrategy = {
    type: 'fitGridWidth'
}
const columnDefs = ref([
    { field: "name_first", headerName: "First Name" },
    { field: "name_last", headerName: "Last Name" },
    { field: "age", headerName: "Age" },
    { field: "throws", headerName: "Throws" },
    { field: "years", headerName: "Years" },
    { field: "wins", headerName: "Wins" },
    { field: "wins_per_year", headerName: "Wins per Year" },
]);
const rowData = ref([]);

// Form related data
const formData = ref({
    maxAge: null,
    minAvgWins: null,
    maxYears: null,
})
const responseMessage = ref("");
const agesList = ref(Array.from({ length: 30 - 20 + 1 }, (_, i) => 20 + i))
const winsList = ref(Array.from({ length: 10 - 1 + 1 }, (_, i) => 1 + i))
const yearsList = ref(Array.from({ length: 10 - 1 + 1 }, (_, i) => 1 + i))

// Handle form submission. Populate the table with the results.
const handleSubmit = async () => {
    if (!formData.value.maxAge || !formData.value.minAvgWins || !formData.value.maxYears) {
        responseMessage.value = "Please make a choice for all options";
        return;
    }
    responseMessage.value = "";

    const response = await fetch(`${apiUrl}/players/top-young-pitchers/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData.value),
    });
    const playerData = await response.json();
    rowData.value = playerData.map((player) => {
        return {
            id: player.id,
            name_first: player.name_first,
            name_last: player.name_last,
            age: player.age,
            throws: player.throws,
            years: player.years,
            wins: player.wins,
            wins_per_year: player.wins_per_year
        }
    })
}
</script>

<template>
    <div class="top-pitchers-container">
        <div class="notes">View top young pitchers who have...</div>
        <form @submit.prevent="handleSubmit">
            <label for="maxAge">1. Maximum age:</label>
            <select id="maxAge" v-model="formData.maxAge">
                <option v-for="option in agesList" :key="option" :value="option">
                {{ option }}
                </option>
            </select>
            <label for="minAvgWins">2. Minimum avg wins per year:</label>
            <select id="minAvgWins" v-model="formData.minAvgWins">
                <option v-for="option in winsList" :key="option" :value="option">
                {{ option }}
                </option>
            </select>
            <label for="maxYears">3. In no more than:</label>
            <select id="maxYears" v-model="formData.maxYears">
                <option v-for="option in yearsList" :key="option" :value="option">
                {{ option }}
                </option>
            </select><span>MLB seasons</span>
            <button type="submit" class="btn btn-secondary btn-sm">
            Submit
            </button>
        </form>
        <div v-if="responseMessage" class="response-message">{{ responseMessage }}</div>
        <div id="tableContainer">
            <ag-grid-vue
                ref="gridRef"
                :rowData="rowData"
                :columnDefs="columnDefs"
                :autoSizeStrategy="autoSizeStrategy"
                :pagination="true"
                :paginationPageSize="10"
                :paginationPageSizeSelector="[10, 25, 50]"
                :theme="themeBalham"
                style="height: 300px"
            >
            </ag-grid-vue>
        </div>
    </div>
</template>

<style scoped>
.top-pitchers-container {
    padding: 10px;
    border-top: .2em solid #ddd;
    text-align: left;
}
.top-pitchers-container select {
    margin-right: .7em;
}
label {
    margin-right: .5em;
}
.notes {
    text-align: left;
    font-weight: bold;
    margin: .2em;
}
button {
    margin-left: 1em;
    margin-bottom: .5em;
}
.response-message {
    font-weight: bold;
    background-color: yellow;
    padding: .3em;
    margin-bottom: 1em;
}
#tableContainer {
    border: .5em solid #BD9B60;
    border-radius: 5px;
}
</style>