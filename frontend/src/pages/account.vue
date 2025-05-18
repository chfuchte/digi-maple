<script setup lang="ts">
import Layout from "@/components/layouts/default.vue";
import { onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";
import { useCurrentUserStore } from "@/stores/user";
import ChangeEmailForm from "@/components/account/ChangeEmailForm.vue";
import ChangeNameForm from "@/components/account/ChangeNameForm.vue";
import ChangePasswordForm from "@/components/account/ChangePasswordForm.vue";
import DeleteAccountForm from "@/components/account/DeleteAccountForm.vue";

const router = useRouter();
const { getUser } = useCurrentUserStore();
const user = ref<Awaited<ReturnType<typeof getUser>>>(null);
onBeforeMount(async () => {
    user.value = await getUser();

    if (!user.value) {
        router.push("/auth");
    }
});
</script>

<template>
    <Layout>
        <div class="flex flex-col items-center justify-center w-full p-4 gap-4">
            <h1 class="text-3xl font-bold">Dein Account</h1>
            <ChangeEmailForm />
            <ChangeNameForm />
            <ChangePasswordForm />
            <DeleteAccountForm />
        </div>
    </Layout>
</template>
