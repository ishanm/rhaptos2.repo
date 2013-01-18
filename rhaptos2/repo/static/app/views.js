// Generated by CoffeeScript 1.3.3
(function() {

  define(['exports', 'underscore', 'backbone', 'marionette', 'jquery', 'aloha', 'app/urls', 'app/controller', './languages', 'hbs!app/views/content-list', 'hbs!app/views/content-list-item', 'hbs!app/views/modal-wrapper', 'hbs!app/views/edit-metadata', 'hbs!app/views/edit-roles', 'hbs!app/views/language-variants', 'hbs!app/views/aloha-toolbar', 'hbs!app/views/sign-in-out', 'i18n!app/nls/strings', 'bootstrap', 'select2'], function(exports, _, Backbone, Marionette, jQuery, Aloha, URLS, Controller, Languages, SEARCH_RESULT, SEARCH_RESULT_ITEM, DIALOG_WRAPPER, EDIT_METADATA, EDIT_ROLES, LANGUAGE_VARIANTS, ALOHA_TOOLBAR, SIGN_IN_OUT, __) {
    var AlohaEditView, DELAY_BEFORE_SAVING, LANGUAGES, METADATA_SUBJECTS, SELECT2_AJAX_HANDLER, SELECT2_MAKE_SORTABLE, languageCode, value, _ref;
    DELAY_BEFORE_SAVING = 3000;
    SELECT2_AJAX_HANDLER = function(url) {
      return {
        quietMillis: 500,
        url: url,
        dataType: 'json',
        data: function(term, page) {
          return {
            q: term
          };
        },
        results: function(data, page) {
          var id;
          return {
            results: (function() {
              var _i, _len, _results;
              _results = [];
              for (_i = 0, _len = data.length; _i < _len; _i++) {
                id = data[_i];
                _results.push({
                  id: id,
                  text: id
                });
              }
              return _results;
            })()
          };
        }
      };
    };
    SELECT2_MAKE_SORTABLE = function($el) {
      return Aloha.ready(function() {
        return $el.select2('container').find('ul.select2-choices').sortable({
          cursor: 'move',
          containment: 'parent',
          start: function() {
            return $el.select2('onSortStart');
          },
          update: function() {
            return $el.select2('onSortEnd');
          }
        });
      });
    };
    METADATA_SUBJECTS = ['Arts', 'Mathematics and Statistics', 'Business', 'Science and Technology', 'Humanities', 'Social Sciences'];
    LANGUAGES = [
      {
        code: '',
        "native": '',
        english: ''
      }
    ];
    _ref = Languages.getLanguages();
    for (languageCode in _ref) {
      value = _ref[languageCode];
      value = jQuery.extend({}, value);
      jQuery.extend(value, {
        code: languageCode
      });
      LANGUAGES.push(value);
    }
    exports.SearchResultItemView = Marionette.ItemView.extend({
      tagName: 'tr',
      template: SEARCH_RESULT_ITEM,
      onRender: function() {
        var _this = this;
        return this.$el.on('click', function() {
          var id;
          id = _this.model.get('id');
          return Controller.editContent(id);
        });
      }
    });
    exports.SearchResultView = Marionette.CompositeView.extend({
      template: SEARCH_RESULT,
      itemViewContainer: 'tbody',
      itemView: exports.SearchResultItemView,
      initialize: function() {
        var _this = this;
        this.listenTo(this.collection, 'reset', function() {
          return _this.render();
        });
        this.listenTo(this.collection, 'update', function() {
          return _this.render();
        });
        this.listenTo(this.collection, 'add', function() {
          return _this.render();
        });
        return this.listenTo(this.collection, 'remove', function() {
          return _this.render();
        });
      }
    });
    AlohaEditView = Marionette.ItemView.extend({
      template: function() {
        throw 'You need to specify a template, modelKey, and optionally alohaOptions';
      },
      modelKey: null,
      alohaOptions: null,
      initialize: function() {
        var _this = this;
        return this.listenTo(this.model, "change:" + this.modelKey, function(model, value) {
          var alohaEditable, alohaId, editableBody;
          alohaId = _this.$el.attr('id');
          if (alohaId && _this.$el.parents()[0]) {
            alohaEditable = Aloha.getEditableById(alohaId);
            editableBody = alohaEditable.getContents();
            if (value !== editableBody) {
              return alohaEditable.setContents(value);
            }
          } else {
            return _this.$el.empty().append(value);
          }
        });
      },
      onRender: function() {
        var updateModelAndSave,
          _this = this;
        this.$el.find('math').wrap('<span class="math-element aloha-cleanme"></span>');
        if (typeof MathJax !== "undefined" && MathJax !== null) {
          MathJax.Hub.Configured();
        }
        this.$el.addClass('disabled');
        Aloha.ready(function() {
          _this.$el.aloha(_this.alohaOptions);
          return _this.$el.removeClass('disabled');
        });
        updateModelAndSave = function() {
          var alohaEditable, alohaId, editableBody;
          alohaId = _this.$el.attr('id');
          if (alohaId) {
            alohaEditable = Aloha.getEditableById(alohaId);
            editableBody = alohaEditable.getContents();
            _this.model.set(_this.modelKey, editableBody);
            if (_this.model.changedAttributes()) {
              return _this.model.save();
            }
          }
        };
        return this.$el.on('blur', updateModelAndSave);
      }
    });
    exports.ContentEditView = AlohaEditView.extend({
      template: function(serialized_model) {
        return "" + (serialized_model.body || 'This module is empty. Please change it');
      },
      modelKey: 'body'
    });
    exports.TitleEditView = AlohaEditView.extend({
      template: function(serialized_model) {
        return "" + (serialized_model.title || 'Untitled');
      },
      modelKey: 'title',
      tagName: 'span'
    });
    exports.ContentToolbarView = Marionette.ItemView.extend({
      template: ALOHA_TOOLBAR,
      onRender: function() {
        var _this = this;
        this.$el.addClass('disabled');
        return Aloha.ready(function() {
          return _this.$el.removeClass('disabled');
        });
      }
    });
    exports.MetadataEditView = Marionette.ItemView.extend({
      template: EDIT_METADATA,
      events: {
        'change *[name=language]': '_updateLanguageVariant'
      },
      initialize: function() {
        var _this = this;
        this.listenTo(this.model, 'change:title', function() {
          return _this._updateTitle();
        });
        this.listenTo(this.model, 'change:language', function() {
          return _this._updateLanguage();
        });
        this.listenTo(this.model, 'change:subjects', function() {
          return _this._updateSubjects();
        });
        return this.listenTo(this.model, 'change:keywords', function() {
          return _this._updateKeywords();
        });
      },
      _updateTitle: function() {
        return this.$el.find('*[name=title]').val(this.model.get('title'));
      },
      _updateLanguage: function() {
        var lang, language;
        language = this.model.get('language') || '';
        lang = language.split('-')[0];
        this.$el.find("*[name=language]").select2('val', lang);
        return this._updateLanguageVariant();
      },
      _updateLanguageVariant: function() {
        var $label, $language, $variant, code, lang, language, variant, variants, _ref1, _ref2;
        $language = this.$el.find('*[name=language]');
        language = this.model.get('language') || '';
        _ref1 = language.split('-'), lang = _ref1[0], variant = _ref1[1];
        if ($language.val() !== lang) {
          lang = $language.val();
          variant = null;
        }
        $variant = this.$el.find('*[name=variantLanguage]');
        $label = this.$el.find('*[for=variantLanguage]');
        variants = [];
        _ref2 = Languages.getCombined();
        for (code in _ref2) {
          value = _ref2[code];
          if (code.slice(0, 2) === lang) {
            jQuery.extend(value, {
              code: code
            });
            variants.push(value);
          }
        }
        if (variants.length > 0) {
          $variant.removeAttr('disabled');
          $variant.html(LANGUAGE_VARIANTS({
            'variants': variants
          }));
          $variant.find("option[value=" + language + "]").attr('selected', true);
          $label.removeClass('hidden');
          return $variant.removeClass('hidden');
        } else {
          $variant.empty().attr('disabled', true);
          $variant.addClass('hidden');
          return $label.addClass('hidden');
        }
      },
      _updateSelect2: function(key) {
        return this.$el.find("*[name=" + key + "]").select2('val', this.model.get(key));
      },
      _updateSubjects: function() {
        return this._updateSelect2('subjects');
      },
      _updateKeywords: function() {
        return this._updateSelect2('keywords');
      },
      onRender: function() {
        var $keywords, $lang, $languages, $subjects, lang, _i, _len;
        this.$el.find('*[name=title]').val(this.model.get('title'));
        $languages = this.$el.find('*[name=language]');
        for (_i = 0, _len = LANGUAGES.length; _i < _len; _i++) {
          lang = LANGUAGES[_i];
          $lang = jQuery('<option></option>').attr('value', lang.code).text(lang["native"]);
          $languages.append($lang);
        }
        $languages.select2({
          placeholder: __('Select a language')
        });
        $subjects = this.$el.find('*[name=subjects]');
        $subjects.select2({
          tags: METADATA_SUBJECTS,
          tokenSeparators: [','],
          separator: '|'
        });
        $keywords = this.$el.find('*[name=keywords]');
        $keywords.select2({
          tags: this.model.get('keywords') || [],
          tokenSeparators: [','],
          separator: '|',
          ajax: SELECT2_AJAX_HANDLER(URLS.KEYWORDS),
          initSelection: function(element, callback) {
            var data;
            data = [];
            _.each(element.val().split('|'), function(str) {
              return data.push({
                id: str,
                text: str
              });
            });
            return callback(data);
          }
        });
        this._updateLanguage();
        this._updateSubjects();
        this._updateKeywords();
        this.delegateEvents();
        return this.$el.find('input[name=title]').focus();
      },
      attrsToSave: function() {
        var keywords, kw, language, subjects, title, variant;
        title = this.$el.find('input[name=title]').val();
        language = this.$el.find('*[name=language]').val();
        variant = this.$el.find('*[name=variantLanguage]').val();
        language = variant || language;
        subjects = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('*[name=subjects]').val().split('|');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw);
          }
          return _results;
        }).call(this);
        if ('' === subjects[0]) {
          subjects = [];
        }
        keywords = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('*[name=keywords]').val().split('|');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw);
          }
          return _results;
        }).call(this);
        if ('' === keywords[0]) {
          keywords = [];
        }
        return {
          title: title,
          language: language,
          subjects: subjects,
          keywords: keywords
        };
      }
    });
    exports.RolesEditView = Marionette.ItemView.extend({
      template: EDIT_ROLES,
      onRender: function() {
        var $authors, $copyrightHolders;
        $authors = this.$el.find('*[name=authors]');
        $copyrightHolders = this.$el.find('*[name=copyrightHolders]');
        $authors.select2({
          tags: this.model.get('authors') || [],
          tokenSeparators: [','],
          separator: '|'
        });
        $copyrightHolders.select2({
          tags: this.model.get('copyrightHolders') || [],
          tokenSeparators: [','],
          separator: '|'
        });
        SELECT2_MAKE_SORTABLE($authors);
        SELECT2_MAKE_SORTABLE($copyrightHolders);
        this._updateAuthors();
        this._updateCopyrightHolders();
        return this.delegateEvents();
      },
      _updateAuthors: function() {
        return this.$el.find('*[name=authors]').select2('val', this.model.get('authors') || []);
      },
      _updateCopyrightHolders: function() {
        return this.$el.find('*[name=copyrightHolders]').select2('val', this.model.get('copyrightHolders') || []);
      },
      attrsToSave: function() {
        var authors, copyrightHolders, kw;
        authors = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('*[name=authors]').val().split('|');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw);
          }
          return _results;
        }).call(this);
        copyrightHolders = (function() {
          var _i, _len, _ref1, _results;
          _ref1 = this.$el.find('*[name=copyrightHolders]').val().split('|');
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            kw = _ref1[_i];
            _results.push(kw);
          }
          return _results;
        }).call(this);
        return {
          authors: authors,
          copyrightHolders: copyrightHolders
        };
      }
    });
    exports.DialogWrapper = Marionette.ItemView.extend({
      template: DIALOG_WRAPPER,
      onRender: function() {
        var _this = this;
        this.options.view.render();
        this.$el.find('.dialog-body').append(this.options.view.$el);
        this.$el.on('click', '.cancel', function() {
          return _this.trigger('cancelled');
        });
        return this.$el.on('click', '.save', function(evt) {
          var attrs;
          evt.preventDefault();
          attrs = _this.options.view.attrsToSave();
          return _this.options.view.model.save(attrs, {
            success: function(res) {
              _this.options.view.model.trigger('sync');
              return _this.trigger('saved');
            },
            error: function(res) {
              return alert('Something went wrong when saving: ' + res);
            }
          });
        });
      }
    });
    exports.AuthView = Marionette.ItemView.extend({
      template: SIGN_IN_OUT,
      events: {
        'click #sign-in': 'signIn',
        'click #sign-out': 'signOut'
      },
      onRender: function() {
        var _this = this;
        this.listenTo(this.model, 'change', function() {
          return _this.render();
        });
        return this.listenTo(this.model, 'change:userid', function() {
          return _this.render();
        });
      },
      signIn: function() {
        return alert('login not supported yet');
      },
      signOut: function() {
        return this.model.signOut();
      }
    });
    exports.WorkspaceView = exports.SearchResultView;
    return exports;
  });

}).call(this);
