<script setup>
import { ref, onMounted } from 'vue'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';


const playerData = ref(null)
const defaultSortBy = "name_last";
const searchField = ["name_first", "name_last"];
const searchValue = ref("");
const headers = [
    // { text: "ID", value: "id" },
    { text: "First Name", value: "name_first" },
    { text: "Last Name", value: "name_last", sortable: true },
    { text: "Use Name", value: "name_use" },
    { text: "Team", value: "team", sortable: true },
    { text: "Birth Date", value: "birth_date" },
    { text: "Height", value: "height_total"},
    { text: "Weight", value: "weight" },
    { text: "Throws", value: "throws" },
    { text: "Bats", value: "bats" },
    { text: "Primary Pos", value: "primary_position", sortable: true },
];
const items = ref([])
const posNames = {
    1: "Pitcher",
    2: "Catcher",
    3: "1st Base",
    4: "2nd Base",
    5: "3rd Base",
    6: "Shortstop",
    7: "Left Field",
    8: "Center Field",
    9: "Right Field",
    "O": "Offence",
    "D": "Defense",
}

onMounted(async () => {
    const response = await fetch("http://127.0.0.1:8000/players/")
    playerData.value = await response.json()
    items.value = playerData.value.map((player) => {
        return {
            id: player.id, 
            name_first: player.name_first,
            name_last: player.name_last,
            name_use: `"${player.name_use}"`,
            team: player.team,
            birth_date: player.birth_date,
            height_total: `${player.height_feet}' - ${player.height_inches ? player.height_inches : '?'}"`,
            weight: `${player.weight} lbs`,
            throws: player.throws,
            bats: player.bats,
            primary_position: `${player.primary_position ? player.primary_position + " - " + posNames[player.primary_position] : "undefined"}`,
        }
    })
})

const showPlayerStats = (item) => {console.log(item.id)}
</script>


<template>
    <div id="searchBox">
    <span>Name search:&nbsp;</span>
    <input type="text" v-model="searchValue">
    <span id="headerNote">Sorting and filtering available in the header</span>
    </div>
    
    <Vue3EasyDataTable 
    :headers="headers"
    :items="items"
    :sort-by="defaultSortBy"
    :search-field="searchField"
    :search-value="searchValue"
    alternating
    buttons-pagination
    @click-row="showPlayerStats"
    >
        <template #empty-message>
            Loading...
        </template>
    </Vue3EasyDataTable>
    <!-- {{ playerData }} -->
</template>

<style scoped>
    #searchBox {
        text-align: left;
        margin-bottom: .5em;
    }
    #headerNote {
        float: right;
        font-size: small;
        font-style: italic;
    }
</style>