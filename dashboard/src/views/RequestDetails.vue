<template>
  <LoggedInTopNav title="حالة الطلب" :backArrow="true" />
  <div
    class="flex items-center justify-center mt-24 lg:mt-40 sm:mt-32 mb-16 pb-16"
  >
    <div
      class="chat-container flex flex-col-reverse w-full gap-4 p-8 mx-0 bg-gray-200 rounded-box"
    >
      <div
        v-if="comments"
        class="message flex flex-col gap-1"
        v-for="(comment, index) in filteredComments"
        :key="`${comment.content} ${index}`"
      >
        <span class="text-xs text-gray-500 text-center">
          {{ formatTimestampTo12Hour(comment.creation) }}
        </span>
        <div
          class="flex flex-row items-start"
          v-if="comment.comment_type == 'Comment'"
        >
          <div
            class="icon bg-white w-11 h-8 flex justify-center items-center rounded-full p-0 m-0"
            v-if="usermail != comment.owner"
          >
            <img
              src="../assets/images/logo.png"
              width="16"
              height="16"
              alt="system-message"
            />
          </div>
          <div
            class="icon bg-white w-11 h-8 flex justify-center items-center rounded-full p-0 m-0 order-1"
            v-else
          >
            <img
              v-if="userData.user_image"
              :src="userData.user_image"
              style="
                width: 40px;
                border-radius: 50%;
                height: 40px;
                object-fit: contain;
              "
              alt="my-message"
            />
            <font-awesome-icon
              v-else
              icon="fa-regular fa-user"
              class="w-4 h-4 text-black"
            />
          </div>
          <div
            class="bg-white p-4 mx-3 rounded-lg shadow w-full"
            v-if="comment?.content?.includes(' || ')"
          >
            <h4 class="text-primary">
              {{
                parseHTML(comment.content)?.split(" || ")[0]?.split("label:")[1]
              }}
            </h4>
            <div class="btns flex flex-row justify-center items-center gap-2">
              <a
                class="btn btn-secondry btn-sm bg-primary border-none hover:bg-primary text-white"
                :href="
                  parseHTML(comment.content)
                    ?.split(' || ')[2]
                    ?.split('link:')[1]
                "
                :target="
                  (() => {
                    const tabValue = parseHTML(comment.content)
                      ?.split(' || ')[1]
                      ?.split('tab:')[1];
                    return tabValue == 1 ? '_self' : '_blank';
                  })()
                "
              >
                عرض
              </a>
            </div>
          </div>
          <div class="bg-white p-4 mx-3 rounded-lg shadow w-full" v-else>
            <p class="text-gray-500">{{ parseHTML(comment.content) }}</p>
          </div>
        </div>
        <div
          class="bg-primaryMoreLight p-5 mx-16 mt-4 rounded-lg shadow flex flex-col justify-center items-center gap-2"
          v-else-if="comment.comment_type == 'Attachment'"
        >
          <h4 class="text-primary">تم إرفاق ملف</h4>
          <div class="btns flex flex-row justify-center items-center gap-2">
            <a
              class="btn btn-secondry btn-sm bg-primary border-none hover:bg-primary text-white"
              :href="getHrefFromContent(comment.content)"
              target="_blank"
            >
              عرض
            </a>
          </div>
        </div>
      </div>

      <h1 v-else class="text-2xl font-bold text-center">لا يوجد أي تعليقات.</h1>
    </div>
  </div>
  <form @submit.prevent="handleSubmit">
    <div class="relative">
      <div
        class="chat-inputs flex justify-between fixed bottom-16 left-0 right-0 bg-white p-4 lg:bottom-0"
      >
        <font-awesome-icon
          v-if="!changeIcon"
          icon="fa-solid fa-paperclip"
          class="p-4 w-4 h-4 mx-2 bg-black text-white rounded-full"
          @click="triggerFileInput"
        />
        <font-awesome-icon
          v-else
          icon="fa-solid fa-circle-check"
          class="p-4 w-4 h-4 mx-2 bg-black text-white rounded-full"
          @click="triggerFileInput"
        />

        <!-- Hidden File Input -->
        <input
          type="file"
          ref="fileInput"
          class="hidden"
          @change="handleFileChange"
        />
        <font-awesome-icon
          icon="fa-solid fa-paper-plane"
          @click="addComment"
          class="p-4 w-4 h-4 mx-2 bg-black text-white rounded-full"
        />
        <input
          type="text"
          class="input input-bordered bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
          placeholder="اكتب رسالة"
          v-model="userComment"
        />
      </div>
    </div>
  </form>
  <BottomNav />
  <Loader v-if="loading" />
</template>

<script setup>
import Loader from "@/components/Loader.vue";
import BottomNav from "@/components/BottomNav.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { useRouter, useRoute } from "vue-router";
import { ref, onMounted, computed } from "vue";
import axios from "axios";

const fileInput = ref(null);
const changeIcon = ref(false);

const triggerFileInput = () => {
  fileInput.value.click();
};

// Router and navigation
const usermail = ref("");
const userComment = ref("");
const loading = ref(false);
const route = useRoute(); // Initialize useRoute to access route parameters
const request_id = route.query.requestId; // Extract requestId from route query
const navigate = useRouter();
const comments = ref(null);

// Request options for fetching logged-in user
const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};

function parseHTML(htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, "text/html");
  return doc.body.textContent || "";
}
const getHrefFromContent = (content) => {
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = content;
  const anchorTag = tempDiv.querySelector("a");
  return anchorTag ? anchorTag.getAttribute("href") : "";
};

const filteredComments = computed(() => {
  return comments.value.filter((comment) => {
    if (comment.comment_type === "Comment") {
      return true;
    }

    if (comment.comment_type === "Attachment") {
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = comment.content;
      const anchor = tempDiv.querySelector("a");
      const fileName = anchor ? anchor.textContent.trim() : "";

      const isRemoved = comments.value.some((delComment) => {
        return (
          delComment.comment_type === "Attachment Removed" &&
          delComment.content.includes(fileName)
        );
      });

      return !isRemoved;
    }

    return false;
  });
});

const isCurrent = ref(true);
const fetchRequests = async () => {
  loading.value = true;
  try {
    const response = await axios.get(
      "/api/method/lsc_api.lsc_api.get_current_requests.get_current_requests"
    );
    if (response.data.message.requests) {
      loading.value = false;
      response.data.message.requests.filter((ele) => {
        if (ele.name === request_id) {
          return (comments.value = ele.comments);
        } else {
          isCurrent.value = false;
        }
      });
    }
  } catch (error) {
    loading.value = false;
    console.error("Failed to fetch requests:", error);
  }
  if (!isCurrent.value) {
    try {
      const response = await axios.get(
        "/api/method/lsc_api.lsc_api.get_previous_requests.get_previous_requests"
      );
      if (response.data.message.requests) {
        loading.value = false;
        response.data.message.requests.filter((ele) => {
          if (ele.name === request_id) {
            return (comments.value = ele.comments);
          } else {
            isCurrent.value = false;
          }
        });
      }
    } catch (error) {
      loading.value = false;
      console.error("Failed to fetch requests:", error);
    }
  }
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    changeIcon.value = true; // Change icon once file is selected
  }
};

const addComment = async () => {
  if (!userComment.value && !changeIcon.value) return;

  loading.value = true;
  try {
    // Post the comment content
    const response = await axios.post(
      "/api/method/lsc_api.lsc_api.create_comment.create_comment",
      { client_transaction: request_id, comment_content: userComment.value },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
  } catch (error) {
    loading.value = false;
    return;
  }

  // Check if a file has been selected for upload
  if (fileInput.value && fileInput.value.files.length > 0) {
    const file = fileInput.value.files[0];
    const formData = new FormData();
    formData.append("client_transaction", request_id);
    formData.append("file", file); // Append the file object itself

    try {
      const fileResponse = await axios.post(
        "/api/method/lsc_api.lsc_api.attach_file.attach_file",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data", // Set to multipart/form-data
          },
          withCredentials: true,
        }
      );
    } catch (fileError) {
      console.error("Failed to upload file:", fileError);
    }
  }

  loading.value = false;
  userComment.value = "";
  fileInput.value.value = ""; // Reset the file input field
  changeIcon.value = false; // Reset the icon state

  fetchRequests(); // Refresh the comments list
};
function formatTimestampTo12Hour(timestamp) {
  // Create a new Date object from the timestamp string
  const date = new Date(timestamp);

  // Get the name of the day (e.g., Monday, Tuesday, etc.)
  const dayName = date.toLocaleDateString("ar-EG", { weekday: "long" });

  // Extract parts of the date
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Months are zero-indexed
  const day = String(date.getDate()).padStart(2, "0");

  // Format hours and minutes
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const ampm = hours >= 12 ? "مساءاً" : "صباحاً";
  hours = hours % 12 || 12; // Convert 24h to 12h format

  // Return the formatted date string with the day name
  return `${hours}:${minutes} ${ampm} -- ${dayName}، ${day}-${month}-${year}`;
}

const userData = ref({
  user_image: null,
});

const getUserData = async () => {
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_user_data.get_user_data"
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    userData.value = data.message.user_data;
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};

// Fetch logged-in user on mount
onMounted(() => {
  getUserData();
  fetchRequests();
  fetch("/api/method/frappe.auth.get_logged_user", requestOptions)
    .then((response) => response.json())
    .then((data) => (usermail.value = data.message))
    .catch(() => navigate.replace("/"));
});
</script>

<style scoped>
.chat-container {
  max-width: 400px;
  margin: 0 auto;
}

.message {
  width: 100%;
}
</style>
