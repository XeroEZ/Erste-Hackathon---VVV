import {
  View,
  Text,
  Image,
  ActivityIndicator,
  TouchableOpacity,
} from "react-native";
import React, { useState, useEffect } from "react";
import { images } from "@/constants/images";
import { router } from "expo-router";

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
          credentials: "include",
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

  // Získanie aktuálneho mesiaca
  const getCurrentMonth = () => {
    const months = [
      "január",
      "február",
      "marec",
      "apríl",
      "máj",
      "jún",
      "júl",
      "august",
      "september",
      "október",
      "november",
      "december",
    ];
    const currentMonth = new Date().getMonth();
    return months[currentMonth];
  };

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <View className="flex-1 px-6 pt-16">
        {loading ? (
          <View className="items-center justify-center flex-1">
            <ActivityIndicator size="large" color="#FFFFFF" />
          </View>
        ) : error ? (
          <View className="items-center justify-center flex-1">
            <Text className="text-red-500 text-lg">{error}</Text>
          </View>
        ) : user ? (
          <View className="flex-1">
            {/* Header */}
            <View className="items-center mb-8">
              <Text className="text-white text-3xl font-bold">
                Vitajte {user.first_name}
              </Text>
            </View>

                        {/* Výdavky za mesiac */}
            <TouchableOpacity
              activeOpacity={0.7}
              onPress={() => router.push("/(tabs)/expenses")}
              className="bg-box rounded-3xl p-8 mb-6 border border-[#2a3550]"
            >
              <Text className="text-white/60 text-base mb-3">
                Výdavky za {getCurrentMonth()}
              </Text>
              <Text className="text-white text-5xl font-bold">100,000€</Text>
            </TouchableOpacity>

            {/* Stav účtu */}
            <TouchableOpacity
              activeOpacity={0.7}
              onPress={() => router.push("/(tabs)/accbalance")}
              className="bg-box rounded-3xl p-8 mb-8 border border-[#2a3550]"
            >
              <Text className="text-white/60 text-base mb-3">Stav účtu</Text>
              <Text className="text-white text-5xl font-bold">
                100,000,000€
              </Text>
            </TouchableOpacity>

            {/* Karta */}
            <TouchableOpacity
              activeOpacity={0.7}
              onPress={() => router.push("/(tabs)/card")}
              className="rounded-3xl overflow-hidden"
            >
              <Image
                source={images.card}
                className="w-full h-56"
                resizeMode="cover"
              />
            </TouchableOpacity>

          </View>
        ) : null}
      </View>
    </View>
  );
}