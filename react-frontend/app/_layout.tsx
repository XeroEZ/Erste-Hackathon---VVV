import { Stack } from "expo-router";
import { useEffect, useState } from "react";
import { router } from "expo-router";
import "./globals.css";

export default function RootLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuthStatus = async () => {
      // DANO AUTH LOGIKU TU
      const authResult = false; // zatial na false aby zobrazilo sign in screen

      setIsAuthenticated(authResult);
    };

    checkAuthStatus();
  }, []);

  useEffect(() => {
    if (isAuthenticated === false) {
      // TIMEOUT FOR AVOIDING NAVIGATION ISSUES
      setTimeout(() => {
        router.replace("/(auth)/onboarding");
      }, 100);
    }
  }, [isAuthenticated]);

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="chats/[id]" />
    </Stack>
  );
}
