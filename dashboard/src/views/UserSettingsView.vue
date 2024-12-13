<template>
  <LoggedInTopNav title="معلومات الحساب" :backArrow="true" />
  <div class="flex flex-col sm:flex-row w-full px-6 gap-5 mt-24 lg:mt-40 pb-24">
    <div
      class="card article bg-white rounded-sm flex-grow px-4 py-10 gap-10 shadow-md"
    >
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
        <div class="profile-img relative w-32 h-32 mx-auto mb-4">
          <div @click="allowEdit ? triggerFileInput() : null">
            <!-- Image Display -->
            <img
              class="max-w-full h-full object-cover"
              :src="userData.user_image || ProfilePic"
              alt="Profile Image"
            />
            <!-- Overlay with Camera Icon -->
            <div
              v-if="allowEdit"
              class="absolute top-0 left-0 w-full h-full bg-white bg-opacity-75 flex items-center justify-center cursor-pointer"
            >
              <font-awesome-icon icon="fa-solid fa-camera" class="text-black" />
            </div>

            <!-- Hidden File Input -->
            <input
              type="file"
              ref="fileInput"
              accept="image/*"
              class="hidden"
              @change="handleFileChange"
            />
          </div>
        </div>
        <!-- Form Fields -->
        <div class="flex flex-col gap-4">
          <div class="flex flex-col md:flex-row gap-4">
            <label class="form-control flex-1 font-bold">
              <div class="label">
                <span class="label-text">البريد الإلكترونى</span>
              </div>
              <input
                type="email"
                placeholder="example@gmail.com"
                autocomplete="email"
                class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
                v-model="userData.email"
                disabled
              />
            </label>
            <label class="form-control flex-1 font-bold">
              <div class="label">
                <span class="label-text">فرع تقديم الخدمات</span>
              </div>
              <input
                type="text"
                class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
                v-model="userData.custom_branch"
                disabled
              />
            </label>
            <label class="form-control flex-1 font-bold">
              <div class="label">
                <span class="label-text">رقم الهوية</span>
              </div>
              <input
                type="tel"
                placeholder="رقم الهوية"
                autocomplete="id"
                maxlength="14"
                class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
                v-model="userData.custom_id_number"
                :disabled="!allowEdit"
              />
            </label>
            <label class="form-control flex-1 font-bold">
              <div class="label">
                <span class="label-text">رقم الجوال</span>
              </div>
              <input
                type="tel"
                placeholder="رقم الجوال"
                autocomplete="tel"
                class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
                v-model="userData.mobile_no"
                :disabled="!allowEdit"
              />
            </label>
            <label class="form-control flex-1 font-bold">
              <div class="label"><span class="label-text">كلمة السر</span></div>
              <input
                type="password"
                autocomplete="current-password"
                placeholder="0000000000"
                class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
                v-model="userData.new_password"
                :disabled="!allowEdit"
              />
            </label>
          </div>
        </div>
        <!-- Save and Edit buttons -->
        <button
          type="submit"
          class="btn btn-success text-white w-full max-w-40 self-center"
          :class="allowEdit ? '' : ' hidden'"
        >
          حفظ التغييرات
        </button>
        <button
          type="button"
          class="btn btn-primary text-white w-full max-w-40 self-center"
          @click="toggleDisable"
          :class="allowEdit ? 'bg-danger' : ''"
        >
          {{ allowEdit ? "تراجع" : "تعديل" }}
        </button>
        <!-- The button to open modal -->
        <label
          for="my_modal_7"
          class="btn bg-danger text-white w-full max-w-40 self-center"
          @click="acceptDelete"
        >
          مسح الحساب
        </label>
        <!-- Put this part before </body> tag -->
        <input type="checkbox" id="my_modal_7" class="modal-toggle" />
        <div class="modal" role="dialog">
          <div class="modal-box text-center">
            <h3 class="text-lg font-bold">هل أنت متأكد من مسح الحساب</h3>
            <p class="py-4">يمكنك التواصل مع خدمة العملاء من هنا.</p>
            <div class="btns-action">
              <!-- The button to open modal -->
              <label
                for="my_custom_modal"
                class="btn bg-danger text-white w-full max-w-40"
                @click="acceptDelete2"
                >أريد مسح الحساب.</label
              >
              <!-- Put this part before </body> tag -->
              <input
                type="checkbox"
                id="my_custom_modal"
                class="modal-toggle"
              />
              <div class="modal" role="dialog">
                <div class="modal-box text-center">
                  <h3 class="text-lg font-bold">لا يمكن الرجوع في هذا</h3>
                  <p class="py-4">ستخسر اشتراكاك ان كنت مشترك.</p>
                  <div class="btns-action">
                    <button
                      class="btn bg-danger"
                      type="button"
                      @click="handleDelete"
                    >
                      تأكيد مسح الحساب
                    </button>
                  </div>
                  <div class="modal-action">
                    <label for="my_custom_modal" class="btn bg-success"
                      >تراجع</label
                    >
                  </div>
                </div>
              </div>
              <div class="modal-action">
                <label for="my_modal_7" class="btn bg-success">تراجع</label>
              </div>
            </div>
          </div>
          <label class="modal-backdrop" for="my_modal_7"></label>
        </div>
      </form>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import Loader from "@/components/Loader.vue";
import ProfilePic from "../assets/images/profile.png";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import BottomNav from "@/components/BottomNav.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const fileInput = ref(null);
const userData = ref({
  email: "",
  mobile_no: null,
  user_image: null,
  custom_id_number: null,
  new_password: null,
});
const allowEdit = ref(false);
const loading = ref(false);
const navigate = useRouter();
const firstWarn = ref(false);
const secondWarn = ref(false);
// Trigger the file input click when the overlay is clicked
const triggerFileInput = () => {
  fileInput.value.click();
};

// Fetch user data on mount
const getUserData = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_user_data.get_user_data"
    );
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    userData.value = data.message.user_data;
  } catch (error) {
    console.error("Error fetching user data:", error);
  } finally {
    loading.value = false;
  }
};

// Handle form submission
const handleSubmit = async () => {
  loading.value = true;
  // Create FormData to handle file uploads
  const formData = new FormData();
  formData.append("email", userData.value.email);
  formData.append("mobile_no", userData.value.mobile_no);
  formData.append("custom_id_number", userData.value.custom_id_number);
  formData.append("new_password", userData.value.new_password);
  if (fileInput.value && fileInput.value.files.length > 0) {
    formData.append("user_image", fileInput.value.files[0]);
  }

  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.update_user_data.update_user_data",
      {
        method: "PATCH",
        body: formData, // Send FormData
      }
    );
    if (!response.ok) throw new Error("Network response was not ok");
  } catch (error) {
    console.error("Error updating user data:", error);
  } finally {
    loading.value = false;
    toggleDisable();
  }
};

// Toggle edit mode
const toggleDisable = () => {
  allowEdit.value = !allowEdit.value;
};

// Handle file change and show the uploaded image as preview
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = (e) => {
      userData.value.user_image = e.target.result;
    };
    reader.readAsDataURL(file); // Store the file in userData for form submission
  }
};

function acceptDelete() {
  firstWarn.value = true;
}
function acceptDelete2() {
  secondWarn.value = true;
}

async function handleDelete() {
  if (firstWarn && secondWarn) {
    const del = JSON.stringify({ access_key: "Disable" });
    await fetch("/api/method/lsc_api.lsc_api.disable_user.disable_user", {
      method: "POST",
      body: del,
      headers: {
        "Content-Type": "application/json",
      },
    });
    navigate.replace("/");
  } else {
    firstWarn.value = false;
    secondWarn.value = false;
  }
}

// Check if user is logged in and load data on component mount
onMounted(() => {
  fetch("/api/method/frappe.auth.get_logged_user", {
    method: "GET",
    headers: { Cookie: document.cookie },
  })
    .then((response) => {
      if (!response.ok) throw new Error("You are not logged in");
      return response.json();
    })
    .catch(() => navigate.replace("/"));

  getUserData();
});
</script>

<style scoped></style>
