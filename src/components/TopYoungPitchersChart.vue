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
const gridThemeCustom = themeBalham.withParams({
    // headerTextColor: "white",
    headerBackgroundColor: "#dddddd",
});
const columnDefs = ref([
    { field: "name_first", headerName: "First Name", flex: 2, minWidth: 80 },
    { field: "name_last", headerName: "Last Name", flex: 2, minWidth: 80 },
    { field: "age", headerName: "Age", flex: 1, minWidth: 35 },
    { field: "throws", headerName: "Throws", flex: 1, minWidth: 60 },
    { field: "years", headerName: "Years", flex: 1, minWidth: 50 },
    { field: "wins", headerName: "Wins", flex: 1, minWidth: 45 },
    { field: "wins_per_year", headerName: "Wins/Year", flex: 1, minWidth: 75 },
])
const rowData = ref([])

// Form related data
const formData = ref({
    maxAge: null,
    minAvgWins: null,
    maxYears: null,
})
const responseMessage = ref("")
const agesList = ref(Array.from({ length: 11 }, (_, i) => 20 + i))
const winsList = ref(Array.from({ length: 10 }, (_, i) => 1 + i))
const yearsList = ref(Array.from({ length: 10 }, (_, i) => 1 + i))

// Handle form submission. Populate the table with the results.
const handleSubmit = async () => {
    if (!formData.value.maxAge || !formData.value.minAvgWins || !formData.value.maxYears) {
        responseMessage.value = "Please make a choice for all options"
        return
    }
    responseMessage.value = ""
    let playerData = null
    try {
        const response = await fetch(`${apiUrl}/players/top-young-pitchers/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData.value),
        })
        playerData = await response.json()
    } catch (err) {
        responseMessage.value = "Error retrieving data: " + err
        return
    }
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
        <div class="fw-bold m-1">View top young pitchers...</div>
        <form @submit.prevent="handleSubmit" class="typ-form">
            <label for="maxAge">1. Maximum age:</label>
            <select id="maxAge" v-model="formData.maxAge">
                <option v-for="option in agesList" :key="option" :value="option">
                {{ option }}
                </option>
            </select><br/>
            <label for="minAvgWins">2. Minimum avg wins per year:</label>
            <select id="minAvgWins" v-model="formData.minAvgWins">
                <option v-for="option in winsList" :key="option" :value="option">
                {{ option }}
                </option>
            </select><br/>
            <label for="maxYears">3. In no more than:</label>
            <select id="maxYears" v-model="formData.maxYears">
                <option v-for="option in yearsList" :key="option" :value="option">
                {{ option }}
                </option>
            </select><span>MLB seasons</span><br/>
            <button type="submit" class="btn btn-secondary btn-sm">
            Submit
            </button>
        </form>
        <div class="border border-secondary border-2 rounded-1">
            <ag-grid-vue
                ref="gridRef"
                :rowData="rowData"
                :columnDefs="columnDefs"
                :autoSizeStrategy="autoSizeStrategy"
                :pagination="true"
                :paginationPageSize="10"
                :paginationPageSizeSelector="[10, 25, 50]"
                :theme="gridThemeCustom"
                style="height: 300px"
            >
            </ag-grid-vue>
        </div>
        <div v-if="responseMessage" class="alert alert-danger">{{ responseMessage }}</div>
    </div>
</template>

<style scoped>
.typ-form {
    margin: .3em;
}
.typ-form * {
    margin: .1em .2em;
}
/* .top-pitchers-container {
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
} */
</style>