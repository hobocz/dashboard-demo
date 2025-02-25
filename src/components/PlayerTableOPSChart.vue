<script setup>
import { ref, defineExpose, watch } from "vue"
import { Line } from "vue-chartjs"
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend } from "chart.js"
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

// Simple color generator
function* getColorGenerator() {
  const colorPalette = ["#FF5733", "#33FF57", "#3357FF", "#F3C300", "#A133FF"];
  let index = 0;
  while (true) {
    yield colorPalette[index % colorPalette.length];
    index++;
  }
}
const getColor = getColorGenerator();

// The selected player data passed from the parent component
const selectedPlayers = ref([])
defineExpose({selectedPlayers});
// Chart data and options
const chartData = ref({})
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
}
const loaded = ref(false)

// This class is used to aggregate batting data objects across
// years, and offer some advanced stats.
// Used by parsePlayerBattingData()
class YearlyBattingStats{
    B1 = 0
    B2 = 0
    B3 = 0
    HR = 0
    H = 0
    BB = 0
    AB = 0
    SF = 0

    addStats(stats){
        this.B2 += stats.doubles
        this.B3 += stats.triples
        this.HR += stats.home_runs
        this.H += stats.hits
        this.B1 += this.H - this.B2 - this.B3 - this.HR
        this.BB += stats.bases_on_balls
        this.AB += stats.at_bats
        this.SF += stats.sacrifice_flies
    }

    totalBases(){
        return this.B1 + (2 * this.B2) + (3 * this.B3) + (4 * this.HR)
    }

    OBP(){
        const result = (this.H + this.BB) / (this.AB + this.BB + this.SF)
        return isNaN(result) ? 0 : parseFloat(result.toFixed(3))
    }

    SLG(){
        const result = this.totalBases() / this.AB
        return isNaN(result) ? 0 : parseFloat(result.toFixed(3))
    }

    OPS(){
        return this.OBP() + this.SLG()
    }
}

// Used by watch(selectedPlayers, ...)
const parsePlayerBattingData = (playerNameStats, newChartData) => {
    // Create a YearlyBattingStats object for each year
    const statsByYear = {}
    playerNameStats.battingStats.forEach((battingStat) => {
        if (!statsByYear.hasOwnProperty(battingStat.year)) {
            statsByYear[battingStat.year] = new YearlyBattingStats()
        }
        statsByYear[battingStat.year].addStats(battingStat)
    })
    // Iterate the YearlyBattingStats and add the data to the newChart
    const newData = {
        label: playerNameStats.playerName,
        backgroundColor: getColor.next().value,
        data: new Array(newChartData.labels.length).fill(null)
    }
    for (const [year, stats] of Object.entries(statsByYear)) {
        let yearIndex = newChartData.labels.indexOf(String(year))
        newData.data[yearIndex] = stats.OPS()
    }
    newChartData.datasets.push(newData)
}

// Watch the selectedPlayers for changes.
// On change, fetch each player's stats
watch(selectedPlayers, (updatedPlayers) => {
    // This is wrapped in an async IIFE to get the intended order of operations
    (async () => {
        if (updatedPlayers.length > 5) { return }
        const newChartData = {labels: [], datasets: []}
        const yearSet = new Set()
        const allPlayersBattingStats = []
        // Running the loop like this instead of forEach, so the subsequent code
        // waits on everything before executing
        await Promise.all(updatedPlayers.map(async (player) => {
            const response = await fetch(`http://127.0.0.1:8000/players/${player.id}/stats`)
            const playerStats = await response.json()
            const pName = player.name_first + " " + player.name_last
            if (playerStats.batting.length == 0) {
                alert(`${pName} has no batting stats`)
            }
            playerStats.batting.forEach((stat) => {
                yearSet.add(String(stat.year))
            })
            allPlayersBattingStats.push({
                playerName: pName,
                battingStats: playerStats.batting
            })
        }))
        newChartData.labels = [...yearSet].sort()

        allPlayersBattingStats.forEach((playerNameStats) => {
            parsePlayerBattingData(playerNameStats, newChartData)
        })
        
        // Replace the old chart data with the new
        chartData.value = newChartData
        loaded.value = true
    })();
}, { deep: true })
</script>

<template>
    <div id="chartContainer">
        <Line 
            v-if="loaded" 
            :data="chartData" 
            :options="chartOptions" 
        />
    </div>
</template>

<style scoped>
#chartContainer{
    background-color: white;
}
</style>