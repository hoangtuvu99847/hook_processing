<template>
  <div>
    <div id="content-wrapper" class="d-flex flex-column">
      <!-- Main Content -->
      <router-view/>
    </div>
    <!-- End of Main Content -->
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
