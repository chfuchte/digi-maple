const publicRoutes = ['/auth', '/maps']

export default defineNuxtRouteMiddleware((to) => {
    for (const route of publicRoutes) {
        if (to.path.startsWith(route) || to.path === "/") return
    }

    // check if user is authenticated
    if (useCurrentUserStore().getUser()) return

    return navigateTo('/auth')
})
