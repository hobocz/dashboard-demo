<script setup>
import { ref, onMounted } from "vue"

const menuOpen = ref(true)
const smMedia = ref(false)

const toggleSidebar = () => {
    console.log(smMedia.value)
    if(!smMedia.value){
        menuOpen.value = !menuOpen.value
    } 
}

const handleMediaQueryChange = (event) => {
    smMedia.value = event.matches
    menuOpen.value = !event.matches
};

onMounted(() => {
    const mediaQuery = window.matchMedia("(max-width: 768px)")
    handleMediaQueryChange(mediaQuery)
    mediaQuery.addEventListener("change", handleMediaQueryChange)
});
</script>

<template>
    <div class="d-flex">
        <!-- Sidebar -->
        <div :class="{ 'collapsed': !menuOpen }"
            class="d-flex flex-column sidebar text-white"
        >
            <router-link to="/" class="nav-link">
                <h4 class="text-center m-2" v-show="menuOpen">Dashboard</h4>
            </router-link>
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/dashboard" class="nav-link text-white">
                        <span class="icon-container" title="Players">
                            <img src="../icons/players-icon.png" alt="Icon">
                        </span>
                        <!-- <i class="bi bi-people-fill" data-bs-toggle="tooltip" title="Players"></i> -->
                        <span v-show="menuOpen" class="ms-2">Players</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/batting" class="nav-link text-white">
                        <span class="icon-container" title="Batting">
                            <img src="../icons/batter-icon.png" alt="Icon">
                        </span>
                        <!-- <i class="bi bi-bar-chart-line-fill" data-bs-toggle="tooltip" title="Batting"></i> -->
                        <span v-show="menuOpen" class="ms-2">Batting</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/pitching" class="nav-link text-white">
                        <span class="icon-container" title="Pitching">
                            <img src="../icons/pitcher-icon.png" alt="Icon">
                        </span>
                        <!-- <i class="bi bi-bar-chart-line-fill" data-bs-toggle="tooltip" title="Pitching"></i> -->
                        <span v-show="menuOpen" class="ms-2">Pitching</span>
                    </router-link>
                </li>
            </ul>
            <div class="card m-3 mt-auto" v-show="menuOpen">
                <img src="https://picsum.photos/100/100" class="card-img-top p-1">
                <div class="card-body">
                    <h5 class="card-title">Random Image</h5>
                    <p class="card-text text-wrap">Some quick example text for this card.</p>
                    <a href="#" class="btn btn-primary">Go somewhere</a>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <main class="flex-grow-1">
            <!-- Navbar -->
            <nav class="navbar navbar-custom">
                <button class="btn btn-light ms-2" @click="toggleSidebar" v-show="!smMedia">
                    <i class="bi bi-list"></i>
                </button>
                <!-- <span class="navbar-brand ms-3">Dashboard</span> -->
            </nav>

            <!-- Router View -->
            <div class="container mt-4">
                <router-view />
            </div>
        </main>
    </div>
</template>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  transition: width 0.3s ease-in-out;
  overflow: hidden;
  white-space: nowrap;
  background-color: #004687;
  padding: 0px;
}
.sidebar.collapsed {
  width: 60px;
}
.navbar-custom {
    background-color: #BD9B60;
    min-height: 60px;
}
.icon-container img {
    width: 32px;
    height: 32px;
    background-color: white;
    padding: .2em;
    border-radius: 5px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 50px;
  }
}
</style>
