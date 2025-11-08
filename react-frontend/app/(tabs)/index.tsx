import { images } from "@/constants/images";
import { Text, View, Image, ActivityIndicator } from "react-native";
import { useEffect, useState } from "react";

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export default function Index() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}api/core/user/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include", // Important for session auth
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch user data");
      }

      const data = await response.json();
      setUser(data);
    } catch (err) {
      console.error("Error fetching user:", err);
      setError("Nepodarilo sa načítať používateľa");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <View className="flex-1 px-4 pt-20">
        {loading ? (
          <View className="items-center justify-center flex-1">
            <ActivityIndicator size="large" color="#FFFFFF" />
          </View>
        ) : error ? (
          <View className="items-center">
            <Text className="text-red-500 text-lg">{error}</Text>
          </View>
        ) : user ? (
          <View className="items-center">
            <Text className="text-white text-3xl font-bold">
              Vitajte, {user.first_name} {user.last_name}!
            </Text>
          </View>
        ) : null}
      </View>
    </View>
  );
}
