import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';
import { fetchDashboard } from '../api/client';

export default function DashboardScreen({ route }) {
  const { token } = route.params;
  const [data, setData] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const result = await fetchDashboard(token);
        setData(result);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  if (!data) return <Text>Loading...</Text>;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>Welcome, {data.profile.name}</Text>
      <Text style={styles.section}>Your Courses:</Text>
      {data.courses.map((c) => (
        <Text key={c.id} style={styles.item}>📘 {c.name}</Text>
      ))}
      <Text style={styles.section}>Achievements:</Text>
      {data.achievements.length === 0 ? (
        <Text>No achievements yet</Text>
      ) : (
        data.achievements.map((a) => <Text key={a.id}>🏅 {a.title}</Text>)
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  header: { fontSize: 22, fontWeight: 'bold', marginBottom: 10 },
  section: { marginTop: 20, fontSize: 18, fontWeight: 'bold' },
  item: { fontSize: 16, marginVertical: 4 },
});
