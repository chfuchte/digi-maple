<template>
    <div class="flex flex-col gap-4 pt-8">
        <h1 class="mb-4 text-3xl font-semibold">Account</h1>
        <RouterLink to="/account/general" class="text-muted-foreground transition-colors hover:text-foreground">
            <h3 class="text-md font-medium">Allgemein</h3>
        </RouterLink>
        <RouterLink to="/account/security" class="text-muted-foreground transition-colors hover:text-foreground">
            <h3 class="text-md font-medium">Sicherheit</h3>
        </RouterLink>
    </div>
</template>
