<template>
  <div id="app">
    <header-bar />
    <div class="container-fluid">
      <div class="row">
        <side-bar v-if="false" />
        <main class="col-md-12 ms-sm-auto col-lg-12 px-md-4 pt-4">
          
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
  name: "App",
  components: { HeaderBar, SideBar },
  data() {
    return {
      servers: [],
    };
  },
  created() {},
  mounted() {},
  methods: {},
};
</script>

<style>
@import "assets/css/dashboard.css";
</style>
