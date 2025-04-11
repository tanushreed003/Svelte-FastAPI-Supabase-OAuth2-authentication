<script lang="ts">
	import { signInWithGoogle, signInWithKakao, signOut, getCurrentUser } from '$lib/auth';
	import { onMount } from 'svelte';
	import type { UserResponse } from '../../backend/app/models';

	let user: UserResponse | null = null;
	let loading: boolean = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			const currentUser = await getCurrentUser();
			if (currentUser) {
				user = currentUser;
			}
		} catch (err) {
			console.error('Error getting user information:', err);
			error = 'An error occurred while getting user information.';
		} finally {
			loading = false;
		}
	});

	async function handleGoogleLogin() {
		try {
			await signInWithGoogle();
		} catch (err) {
			console.error('Error during Google login:', err);
			error = 'An error occurred during Google login.';
		}
	}

	async function handleKakaoLogin() {
		try {
			await signInWithKakao();
		} catch (err) {
			console.error('Error during Kakao login:', err);
			error = 'An error occurred during Kakao login.';
		}
	}

	async function handleLogout() {
		try {
			await signOut();
			user = null;
		} catch (err) {
			console.error('Error during logout:', err);
			error = 'An error occurred during logout.';
		}
	}
</script>

<div class="flex h-screen w-full flex-col items-center justify-center bg-gray-50">
	{#if error}
		<div class="mb-4 w-full max-w-md px-4">
			<div class="rounded-lg bg-red-100 p-4 text-sm text-red-800">
				<span class="font-medium">Error!</span>
				{error}
			</div>
		</div>
	{/if}

	{#if loading}
		<div class="flex items-center justify-center">
			<div
				class="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"
			></div>
			<span class="ml-2">Loading...</span>
		</div>
	{:else if user}
		<div class="rounded-lg bg-white p-8 shadow-lg">
			<div class="flex flex-col items-center">
				<h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Welcome!</h2>

				<div class="mb-4 flex flex-col items-center">
					<div
						class="mb-4 flex h-24 w-24 items-center justify-center rounded-full bg-gray-200 text-2xl font-bold text-gray-600"
					>
						{user.email ? user.email[0].toUpperCase() : '?'}
					</div>

					<div class="mb-2 text-lg font-semibold text-gray-800">
						{user.display_name || 'User'}
					</div>
					<div class="mb-2 text-sm text-gray-600">{user.email}</div>
					<div class="mb-6 text-xs text-gray-500">Provider: {user.provider}</div>
				</div>

				<button
					class="flex items-center justify-center gap-2 rounded-md bg-red-500 px-6 py-3 text-base font-medium text-white shadow-md transition-all duration-200 hover:bg-red-600 hover:shadow-lg focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:outline-none"
					on:click={handleLogout}
				>
					<svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M16 17L21 12L16 7"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
						<path
							d="M21 12H9"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
					<span>Logout</span>
				</button>
			</div>
		</div>
	{:else}
		<div class="rounded-lg bg-white p-8 shadow-lg">
			<h2 class="mb-6 text-center text-2xl font-bold text-gray-800">OAuth2 Login</h2>
			<div class="flex flex-col gap-4">
				<button
					class="flex w-64 items-center justify-center gap-2 rounded-md border-none bg-[#4285f4] px-6 py-3 text-base font-medium text-white shadow-md transition-all duration-200 hover:bg-[#3367d6] hover:shadow-lg focus:ring-2 focus:ring-[#4285f4] focus:ring-offset-2 focus:outline-none"
					on:click={handleGoogleLogin}
				>
					<svg class="h-5 w-5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z"
							fill="currentColor"
						/>
					</svg>
					<span>Login with Google</span>
				</button>
				<button
					class="flex w-64 items-center justify-center gap-2 rounded-md border-none bg-[#fee500] px-6 py-3 text-base font-medium text-black shadow-md transition-all duration-200 hover:bg-[#ffdc00] hover:shadow-lg focus:ring-2 focus:ring-[#fee500] focus:ring-offset-2 focus:outline-none"
					on:click={handleKakaoLogin}
				>
					<svg class="h-5 w-5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M12 3C7.031 3 3 6.156 3 10.025C3 12.775 4.931 15.131 7.619 16.3L6.638 19.662C6.594 19.781 6.656 19.912 6.769 19.975C6.85 20.019 6.95 20.013 7.031 19.962L11.044 17.275H12C16.969 17.275 21 14.119 21 10.025C21 6.156 16.969 3 12 3Z"
							fill="currentColor"
						/>
					</svg>
					<span>Login with Kakao</span>
				</button>
			</div>
		</div>
	{/if}
</div>
