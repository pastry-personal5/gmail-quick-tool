from rename_private_labels.rename_private_labels import get_new_label_if_possible

def test_get_new_label_if_possible_0001():
  old_label = {
    'id': 'foo',
    'name': '지난여행/88. SFO-DEC-1959'
  }
  new_label = get_new_label_if_possible(old_label)

  assert new_label is not None
  assert "id" in new_label
  assert new_label["id"] == old_label["id"]
  assert "name" in new_label
  assert new_label["name"] == "지난여행/88. 1959-12-SFO"

def test_get_new_label_if_possible_0002():
  old_label = {
    'id': 'foo',
    'name': 'barbaz'
  }
  new_label = get_new_label_if_possible(old_label)

  assert new_label is None
  