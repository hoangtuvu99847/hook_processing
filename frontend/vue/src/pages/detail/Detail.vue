<template>
  <div>
    <div id="content-wrapper" class="d-flex flex-column">
      <!-- Main Content -->
      <div id="content">
        <div class="container-fluid">
          <ul class="nav nav-tabs mb-2">
            <li class="nav-item">
              <a
                :class="['nav-link', endPoint === 'resources' ? 'active' : '']"
                href="resources"
              >
                Resources
              </a>
            </li>
            <li class="nav-item">
              <a
                :class="['nav-link', endPoint === 'process' ? 'active' : '']"
                href="process"
                >Process</a
              >
            </li>
            <li class="nav-item">
              <a
                :class="['nav-link', endPoint === 'logs' ? 'active' : '']"
                href="logs"
                >Logs</a
              >
            </li>
          </ul>
          <!-- Content Row -->
          <router-view />
        </div>
      </div>
      <!-- End of Main Content -->
    </div>
  </div>
</template>

<script>
export default {
  name: "Detail",
  data() {
    return {
      endPoint: "",
    };
  },
  created() {
    console.log(this.$route.path);
    this.endPoint = this.$route.path.split("/").slice(-1)[0];
  },
  methods: {
    navigateResource() {
      this.$router.push({
        name: "resource",
      });
    },
    navigateProcess() {
      this.$router.push({
        name: "process",
      });
    },
  },
  watch: {
    endPoint: function (val) {
      console.log(val);
    },
  },
};
</script>

<style scoped>
</style>
