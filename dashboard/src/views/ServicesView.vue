<template>
  <LoggedInTopNav title="الخدمات" :backArrow="false" />

  <!-- Service Names at the top -->
  <div class="bg-white mx-4 rounded mb-8 lg:mb-20 mt-24 lg:mt-40">
    <div class="typeOfService flex overflow-y-scroll py-1">
      <span
        v-for="(service, index) in services"
        :key="index"
        :class="{ activeService: activeIndex === index }"
        @click="setActive(index)"
      >
        {{ service.name }}
      </span>
    </div>
  </div>

  <!-- Service Details -->
  <div
    class="openServices grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 lg:gap-17 gap-4 mb-20 overflow-y-scroll mx-4"
  >
    <div
      v-if="currentDepartmentDetails"
      v-for="(elemnt, index) in currentDepartmentDetails"
      :key="index"
      class="openServiceCard text-center flex flex-col gap-2 justify-between items-center bg-white rounded py-4 px-4 lg:py-7"
    >
      <div class="flex justify-between items-center w-full">
        <h1 class="text-black font-bold">{{ elemnt.name }}</h1>
        <h1>
          التكلفة:
          {{ elemnt.hrs }}
          س
        </h1>
      </div>
      <RouterLink
        :to="{
          path: getMatchedPath(elemnt.name),
          query: { elemnt: elemnt.name },
        }"
        class="btn btn-sm w-full bg-primary border-primary rounded h-8 text-white"
      >
        احجز الان
      </RouterLink>
    </div>

    <div
      v-else-if="currentDepartmentDetails != []"
      class="openServiceCard text-center flex flex-col gap-2 justify-between items-center bg-white rounded py-4 px-4 lg:py-7"
    >
      <p class="text-black font-bold">أنت غير مشترك في أي باقة</p>
      <RouterLink
        :to="{
          path: '/packages',
        }"
        class="btn btn-sm w-full bg-primary border-primary rounded h-8 text-white"
      >
        اشترك الان
      </RouterLink>
    </div>
  </div>

  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { useRouter } from "vue-router";

const loading = ref(false);
const navigate = useRouter();
const services = ref([]);
const currentDepartmentDetails = ref(null);
const activeIndex = ref(0);

// Fetch departments and services
const fetchData = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_departments.get_departments"
    );
    const data = await response.json();
    loading.value = false;
    if (data.message.status !== "fail") {
      services.value = data.message.departments.sort((a, b) =>
        b.name.localeCompare(a.name, "ar")
      );
      setActive(0); // Set the first department as active initially
    }
  } catch (error) {
    loading.value = false;
    console.error("Error fetching data:", error);
  }
};

// Set the active service based on the clicked index
const setActive = (index) => {
  activeIndex.value = index;
  currentDepartmentDetails.value = services.value[index]?.details || null;
};

// Get the appropriate path for the service detail
const getMatchedPath = (title) => {
  if (!title) return;
  if (title.includes("دراسة")) {
    return "/services/study-case";
  } else if (title.includes("خدمات")) {
    return "/services/legal";
  } else if (title.includes("قضايا")) {
    return "/services/case";
  } else {
    return "/services/consultation";
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
span {
  @apply text-primary px-6 mx-2 my-2 p-2 text-nowrap rounded duration-300 cursor-pointer;
}

span.activeService {
  @apply bg-primary text-white font-body;
}
</style>
