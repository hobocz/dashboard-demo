<script setup>

import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend } from 'chart.js'
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)


const props = defineProps(['player'])
const chartData = ref({
    labels: [],
    datasets: [
        {
            label: "",
            // backgroundColor: '#f87979',
            data: []
        }
    ]
})
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
}
const loaded = ref(false)


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
        return (this.H + this.BB) / (this.AB + this.BB + this.SF)
    }

    SLG(){
        return this.totalBases() / this.AB
    }

    OPS(){
        return (this.OBP() + this.SLG()).toFixed(3)
    }
}

const parseData = (playerStats) => {
    const statsByYear = {}
    playerStats.batting.forEach((battingStat) => {
        if (!statsByYear.hasOwnProperty(battingStat.year)) {
            statsByYear[battingStat.year] = new YearlyBattingStats()
        }
        statsByYear[battingStat.year].addStats(battingStat)
    })
    chartData.value.datasets[0].label = props.player.name_first + " " + props.player.name_last
    for (const [year, stats] of Object.entries(statsByYear)) {
        chartData.value.labels.push(String(year))
        chartData.value.datasets[0].data.push(stats.OPS())
    }
}

onMounted(async () => {
    const response = await fetch(`http://127.0.0.1:8000/players/${props.player.id}/stats`)
    const playerStats = await response.json()
    parseData(playerStats)
    loaded.value = true
})

</script>


<template>
    <div id="chartContainer">
        <Line v-if="loaded" :data="chartData" :options="chartOptions" />
        <h3 v-else id="loading">Loading...</h3>
    </div>
</template>


<style scoped>
#chartContainer{
    background-color: white;
}
#loading {
    color: black;
}
</style>