<template>
  <div>
    <div id="content-wrapper" class="d-flex flex-column">
      <!-- Main Content -->
      <div id="content">
        <!-- Topbar -->
        <!-- End of Topbar -->

        <!-- Begin Page Content -->
        <div class="container-fluid">
          <ul class="nav nav-tabs mb-2">
            <li class="nav-item">
              <button class="nav-link active" @click="navigateResource">
                Resources
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" @click="navigateProcess">Process</button>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Process</a>
            </li>
          </ul>
          <!-- Content Row -->
          <router-view />
        </div>
        <!-- /.container-fluid -->
      </div>
      <!-- End of Main Content -->
    </div>
  </div>
</template>

<script>
export default {
  name: "Detail",
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
};
</script>

<style scoped>
</style>
