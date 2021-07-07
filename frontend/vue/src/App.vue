<template>
  <div id="app">
    <header-bar/>
    <div class="container-fluid">
      <div class="row">
        <side-bar/>
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          <div
              class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Dashboard</h1>
            <div class="btn-toolbar mb-2 mb-md-0">
              <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary">Share</button>
                <button type="button" class="btn btn-sm btn-outline-secondary">Export</button>
              </div>
              <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
                <span data-feather="calendar"></span>
                This week
              </button>
            </div>
          </div>
          <!--          NAVIGATION HERE-->
          <router-view></router-view>
        </main>
      </div>
    </div>
  </div>
</template>

<script>


import SideBar from "@/components/SideBar";
import HeaderBar from "@/components/HeaderBar";

export default {
  name: 'App',
  components: {HeaderBar, SideBar},
  data() {
    return {
      servers: []
    }
  },
  created() {
  },
  mounted() {

  },
  methods: {}
}
</script>

<style>
@import "assets/css/dashboard.css";
</style>
