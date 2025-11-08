import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import React, { useState, useEffect } from "react";
import { images } from "@/constants/images";
import { icons } from "@/constants/icons";
import { router } from "expo-router";

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

const transactions = [
  { id: 1, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 2, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 3, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 4, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 5, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 6, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
  { id: 7, name: "Nazov organizacie", amount: "35.09€", date: "01. 04. 2025" },
];

export default function Account() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

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
      Alert.alert("Chyba", "Nepodarilo sa načítať používateľa");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View className="flex-1 bg-black items-center justify-center">
        <ActivityIndicator size="large" color="#FFFFFF" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      {/* Header */}
      <View className="flex-row items-center px-5 pt-12 pb-4 border-b border-white/10">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Image
            source={icons.back}
            className="w-6 h-6"
            tintColor="#FFFFFF"
            resizeMode="contain"
          />
        </TouchableOpacity>
        <Text className="text-white text-lg font-semibold flex-1">
          Stav účtu
        </Text>
      </View>

      <ScrollView
        className="flex-1"
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        <View className="px-6 pt-6">
          {/* Stav účtu card */}
          <View className="bg-box rounded-3xl p-6 mb-6 border border-[#2a3550]">
            <Text className="text-white/60 text-sm mb-2">Stav účtu</Text>
            <Text className="text-white text-4xl font-bold">100,000,000€</Text>
          </View>

          {/* Transakcie button */}
          <TouchableOpacity
            activeOpacity={0.7}
            className="bg-box rounded-full px-6 py-3 mb-6 border border-[#2a3550] self-start"
          >
            <Text className="text-white text-base font-medium">
              Transakcie
            </Text>
          </TouchableOpacity>

          {/* Transakcie list */}
          <View>
            {transactions.map((transaction) => (
              <TouchableOpacity
                key={transaction.id}
                activeOpacity={0.7}
                className="flex-row items-center bg-box rounded-2xl p-4 mb-3 border border-[#2a3550]"
              >
                <View className="w-12 h-12 rounded-full bg-red-500 items-center justify-center mr-4">
                  <Text className="text-white text-2xl">🎭</Text>
                </View>
                <View className="flex-1">
                  <Text className="text-white text-base font-medium">
                    {transaction.name}
                  </Text>
                  <Text className="text-white/50 text-xs mt-1">
                    {transaction.date}
                  </Text>
                </View>
                <View className="items-end">
                  <Text className="text-white text-lg font-semibold">
                    {transaction.amount}
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>
    </View>
  );
}